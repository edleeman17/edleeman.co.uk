import express from 'express';
import { execSync } from 'child_process';
import { writeFileSync } from 'fs';
import { join } from 'path';

const app = express();
const REPO = process.env.REPO_PATH;
const TOKEN = process.env.BEARER_TOKEN;
const SITE_URL = process.env.SITE_URL || 'https://edleeman.co.uk';

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

function auth(req, res, next) {
  const header = req.headers.authorization || '';
  if (header !== `Bearer ${TOKEN}`) return res.status(401).json({ error: 'unauthorized' });
  next();
}

// iA Writer queries config before publishing
app.get('/micropub', auth, (req, res) => {
  if (req.query.q === 'config') {
    return res.json({ 'syndicate-to': [{ uid: 'mastodon', name: 'Mastodon' }] });
  }
  res.json({});
});

// Token verification endpoint (iA Writer may query this on setup)
app.get('/token', (req, res) => {
  const header = req.headers.authorization || '';
  if (header === `Bearer ${TOKEN}`) {
    return res.json({ me: SITE_URL, scope: 'create', access_token: TOKEN });
  }
  res.status(401).json({ error: 'unauthorized' });
});

// Create content
app.post('/micropub', auth, (req, res) => {
  try {
    const body = req.body;
    const now = new Date();
    const iso = now.toISOString();
    const datePart = iso.slice(0, 10);
    const timePart = now.toTimeString().slice(0, 8).replace(/:/g, '');

    const bookmarkOf = body['bookmark-of'];
    const name = body['name'];
    const postContent = body['content'] || '';

    let filename, content, urlPath;

    if (bookmarkOf) {
      const slug = slugify(name || bookmarkOf).slice(0, 60);
      const ts = Date.now();
      filename = `content/links/${datePart}-${ts}-${slug}.md`;
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
        '---',
        '',
      ].join('\n');

    } else if (name) {
      const slug = slugify(name);
      filename = `content/posts/${datePart}-${slug}.md`;
      urlPath = `/posts/${slug}/`;
      content = [
        '---',
        `title: "${esc(name)}"`,
        `date: ${iso}`,
        `draft: false`,
        `type: "post"`,
        `syndication: []`,
        '---',
        '',
        postContent,
        '',
      ].join('\n');

    } else {
      const slug = `${datePart}-${timePart}`;
      filename = `content/notes/${slug}.md`;
      urlPath = `/notes/${slug}/`;
      content = [
        '---',
        `title: ""`,
        `date: ${iso}`,
        `draft: false`,
        `type: "note"`,
        `slug: "${slug}"`,
        `syndication: []`,
        '---',
        '',
        postContent,
        '',
      ].join('\n');
    }

    writeFileSync(join(REPO, filename), content, 'utf8');
    execSync(`git -C ${REPO} add ${filename}`);
    execSync(`git -C ${REPO} commit -m "micropub: add ${filename}"`);
    execSync(`git -C ${REPO} push`);

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
