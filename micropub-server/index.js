import express from 'express';
import { execSync } from 'child_process';
import { writeFileSync, mkdirSync } from 'fs';
import { join, extname } from 'path';
import multer from 'multer';

const app = express();
const REPO = process.env.REPO_PATH;
const TOKEN = process.env.BEARER_TOKEN;
const SITE_URL = process.env.SITE_URL || 'https://edleeman.co.uk';
const MEDIA_ENDPOINT = process.env.MEDIA_ENDPOINT || 'https://micropub.lan/micropub/media';

const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 20 * 1024 * 1024 } });

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use((req, res, next) => { if (req.method === 'POST') console.log('POST body:', JSON.stringify(req.body)); next(); });

function auth(req, res, next) {
  const header = req.headers.authorization || '';
  if (header !== `Bearer ${TOKEN}`) return res.status(401).json({ error: 'unauthorized' });
  next();
}

function gitSync(relPath) {
  execSync(`git -C ${REPO} pull --rebase --autostash`);
  execSync(`git -C ${REPO} add ${relPath}`);
  execSync(`git -C ${REPO} commit -m "micropub: add ${relPath}"`);
  execSync(`git -C ${REPO} push`);
}

app.get('/micropub', auth, (req, res) => {
  if (req.query.q === 'config') {
    return res.json({
      'media-endpoint': MEDIA_ENDPOINT,
      'syndicate-to': [{ uid: 'mastodon', name: 'Mastodon' }],
    });
  }
  res.json({});
});

app.get('/token', (req, res) => {
  const header = req.headers.authorization || '';
  if (header === `Bearer ${TOKEN}`) {
    return res.json({ me: SITE_URL, scope: 'create media', access_token: TOKEN });
  }
  res.status(401).json({ error: 'unauthorized' });
});

app.post('/micropub/media', auth, upload.single('file'), (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: 'no file' });

    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const ts = Date.now();
    const ext = extname(req.file.originalname).toLowerCase() || '.jpg';
    const safeName = req.file.originalname
      .replace(/\.[^.]+$/, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 40);
    const filename = `${ts}-${safeName}${ext}`;
    const relPath = `static/images/${year}/${month}/${filename}`;
    const publicUrl = `${SITE_URL}/images/${year}/${month}/${filename}`;

    mkdirSync(join(REPO, `static/images/${year}/${month}`), { recursive: true });
    writeFileSync(join(REPO, relPath), req.file.buffer);
    gitSync(relPath);

    res.status(201).set('Location', publicUrl).json({ url: publicUrl });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

function parseProps(body) {
  if (body.properties) {
    const p = body.properties;
    return {
      name: p.name?.[0],
      content: p.content?.[0],
      'bookmark-of': p['bookmark-of']?.[0],
    };
  }
  return { name: body.name, content: body.content, 'bookmark-of': body['bookmark-of'] };
}

app.post('/micropub', auth, (req, res) => {
  try {
    const props = parseProps(req.body);
    const now = new Date();
    const iso = now.toISOString();
    const datePart = iso.slice(0, 10);
    const timePart = now.toTimeString().slice(0, 8).replace(/:/g, '');

    const bookmarkOf = props['bookmark-of'];
    const postContent = props['content'] || '';
    // iA Writer always sends name — only treat as post if content has an explicit # Heading
    const rawName = props['name'];
    const hasHeading = postContent.startsWith('# ') || /\n# /.test(postContent);
    const name = hasHeading ? rawName : undefined;

    let relPath, content, urlPath;

    if (bookmarkOf) {
      const slug = slugify(name || bookmarkOf).slice(0, 60);
      const ts = Date.now();
      relPath = `content/links/${datePart}-${ts}-${slug}.md`;
      urlPath = `/links/${datePart}-${ts}-${slug}/`;
      content = [
        '---',
        `title: "${esc(name || '')}"`,
        `link: "${bookmarkOf}"`,
        `description: "${esc(postContent)}"`,
        `date: ${iso}`,
        `category: "Interesting"`,
        `syndicate: true`,
        `syndication: []`,
        '---', '',
      ].join('\n');

    } else if (name) {
      const slug = slugify(name);
      relPath = `content/posts/${datePart}-${slug}.md`;
      urlPath = `/posts/${slug}/`;
      content = [
        '---',
        `title: "${esc(name)}"`,
        `date: ${iso}`,
        `draft: false`,
        `type: "post"`,
        `syndication: []`,
        '---', '',
        postContent, '',
      ].join('\n');

    } else {
      const slug = `${datePart}-${timePart}`;
      relPath = `content/notes/${slug}.md`;
      urlPath = `/notes/${slug}/`;
      content = [
        '---',
        `title: ""`,
        `date: ${iso}`,
        `draft: false`,
        `type: "note"`,
        `slug: "${slug}"`,
        `syndication: []`,
        '---', '',
        postContent, '',
      ].join('\n');
    }

    writeFileSync(join(REPO, relPath), content, 'utf8');
    gitSync(relPath);

    res.status(201).set('Location', `${SITE_URL}${urlPath}`).json({ url: `${SITE_URL}${urlPath}` });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

function slugify(str) {
  return String(str).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function esc(str) {
  return String(str).replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

app.listen(3000, () => console.log('micropub :3000'));
