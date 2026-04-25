---
title: "About me"
type: page
---

<h1>About me <span id="live-age" data-pagefind-ignore style="color: var(--color-text-muted)"></span></h1>

Software Engineer, Self Hoster, DevOpser, Photographer, Dad

<script>
(function() {
  var birth = new Date('1998-01-01T00:00:00');
  var el = document.getElementById('live-age');
  function update() {
    var ms = Date.now() - birth.getTime();
    var years = ms / (365.25 * 24 * 60 * 60 * 1000);
    el.textContent = years.toFixed(9);
  }
  update();
  setInterval(update, 100);
})();
</script>

Email: [hello@edleeman.co.uk](mailto:hello@edleeman.co.uk)

To send me an encrypted email, my OpenPGP public key is available on public keyservers. Modern email clients should pick it up automatically. If not, you can find my public key [here](https://edleeman.co.uk/.well-known/publickey.txt)

Key ID: 0x5C8C3EF2838E6186

PGP Fingerprint: 9506 7F25 B68B EB77 E09D  DCD2 5C8C 3EF2 838E 6186
