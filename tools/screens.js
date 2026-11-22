// Renders the app screens shown on the site (iPhone 15/16 size, 1179×2556) in every site language:
//   NODE_PATH=<dir with playwright> PW_CHANNEL=chrome node tools/screens.js   (Node 20+, needs cwebp)
// The layout mirrors the app's chat screen; the answers are written to match what the app returns.
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const ROOT = path.join(__dirname, '..');

const UI = {
  en: ['Close', 'New Chat', 'Enter message…', 'What is the story behind this artwork?'],
  tr: ['Kapat', 'Yeni Sohbet', 'Mesaj yazın…', 'Bu eserin hikâyesi ne?'],
  fr: ['Fermer', 'Nouvelle discussion', 'Écrire un message…', 'Quelle est l’histoire de cette œuvre ?'],
  de: ['Schließen', 'Neuer Chat', 'Nachricht eingeben…', 'Was ist die Geschichte dieses Kunstwerks?'],
  es: ['Cerrar', 'Nuevo chat', 'Escribe un mensaje…', '¿Cuál es la historia de esta obra?'],
};
const L = { en: ['Title', 'Artist', 'Date', 'Where'], tr: ['Eser', 'Sanatçı', 'Tarih', 'Nerede'],
  fr: ['Titre', 'Artiste', 'Date', 'Où'], de: ['Titel', 'Künstler', 'Datum', 'Wo'], es: ['Título', 'Artista', 'Fecha', 'Dónde'] };

const SCENES = [
  { img: 'mona-lisa', pos: 'center 30%', kv: ['Mona Lisa', 'Leonardo da Vinci', 'c. 1503–1519', { en: 'Louvre, Paris', tr: 'Louvre, Paris', fr: 'Louvre, Paris', de: 'Louvre, Paris', es: 'Louvre, París' }],
    t: { en: ['This is the <b>Mona Lisa</b> (La Gioconda), the most famous portrait in the world.', 'Leonardo worked on it for years. Look at the <b>sfumato</b>: soft, smoky transitions around her eyes and mouth that make her smile seem to change as you look.'],
         tr: ['Bu, dünyanın en ünlü portresi <b>Mona Lisa</b> (La Gioconda).', 'Leonardo yıllarca üzerinde çalıştı. Göz ve dudak çevresindeki yumuşak, dumanlı geçişlere, yani <b>sfumato</b>ya bakın: gülümsemesi baktıkça değişiyor gibi görünür.'],
         fr: ['Voici <b>La Joconde</b> (Mona Lisa), le portrait le plus célèbre du monde.', 'Léonard y a travaillé pendant des années. Observez le <b>sfumato</b> : ces transitions vaporeuses autour des yeux et de la bouche qui font varier son sourire.'],
         de: ['Das ist die <b>Mona Lisa</b> (La Gioconda), das berühmteste Porträt der Welt.', 'Leonardo arbeitete jahrelang daran. Achte auf das <b>Sfumato</b>: weiche, rauchige Übergänge um Augen und Mund, durch die ihr Lächeln sich zu verändern scheint.'],
         es: ['Es la <b>Mona Lisa</b> (La Gioconda), el retrato más famoso del mundo.', 'Leonardo trabajó en ella durante años. Fíjate en el <b>sfumato</b>: transiciones suaves y difuminadas en ojos y boca que hacen que su sonrisa parezca cambiar.'] } },
  { img: 'starry-night', pos: 'center', kv: [{ en: 'The Starry Night', tr: 'Yıldızlı Gece', fr: 'La Nuit étoilée', de: 'Die Sternennacht', es: 'La noche estrellada' }, 'Vincent van Gogh', '1889', { en: 'MoMA, New York', tr: 'MoMA, New York', fr: 'MoMA, New York', de: 'MoMA, New York', es: 'MoMA, Nueva York' }],
    t: { en: ['This is <b>The Starry Night</b> by Vincent van Gogh.', 'He painted it at the asylum in Saint-Rémy, from the view outside his window before sunrise, adding the village from imagination. The swirling sky and the flame-like cypress make it one of the icons of <b>Post-Impressionism</b>.'],
         tr: ['Bu, Vincent van Gogh’un <b>Yıldızlı Gece</b> tablosu.', 'Saint-Rémy’deki akıl hastanesinde, gün doğmadan önce penceresinden gördüğü manzarayı resmetti; köyü hayal gücüyle ekledi. Kıvrılan gökyüzü ve alev gibi selvi onu <b>Post-Empresyonizm</b>in simgelerinden biri yapar.'],
         fr: ['Voici <b>La Nuit étoilée</b> de Vincent van Gogh.', 'Il l’a peinte à l’asile de Saint-Rémy, d’après la vue de sa fenêtre avant l’aube, en inventant le village. Le ciel tourbillonnant et le cyprès en flamme en font une icône du <b>postimpressionnisme</b>.'],
         de: ['Das ist <b>Die Sternennacht</b> von Vincent van Gogh.', 'Er malte sie in der Heilanstalt von Saint-Rémy nach dem Blick aus seinem Fenster vor Sonnenaufgang; das Dorf ergänzte er aus der Fantasie. Der wirbelnde Himmel und die flammenartige Zypresse machen sie zur Ikone des <b>Postimpressionismus</b>.'],
         es: ['Es <b>La noche estrellada</b> de Vincent van Gogh.', 'La pintó en el sanatorio de Saint-Rémy, a partir de la vista desde su ventana antes del amanecer, e inventó el pueblo. El cielo en remolinos y el ciprés como una llama la convierten en un icono del <b>postimpresionismo</b>.'] } },
  { img: 'birth-of-venus', pos: 'center 40%', kv: [{ en: 'The Birth of Venus', tr: 'Venüs’ün Doğuşu', fr: 'La Naissance de Vénus', de: 'Die Geburt der Venus', es: 'El nacimiento de Venus' }, 'Sandro Botticelli', 'c. 1484–1486', { en: 'Uffizi, Florence', tr: 'Uffizi, Floransa', fr: 'Offices, Florence', de: 'Uffizien, Florenz', es: 'Uffizi, Florencia' }],
    t: { en: ['This is <b>The Birth of Venus</b> by Sandro Botticelli.', 'The goddess arrives on a scallop shell, blown ashore by the winds while a nymph waits with a cloak. Painted on canvas, unusual in Florence at the time, it is a highlight of the <b>Early Renaissance</b>.'],
         tr: ['Bu, Sandro Botticelli’nin <b>Venüs’ün Doğuşu</b> tablosu.', 'Tanrıça, rüzgârların kıyıya ittiği bir istiridye kabuğunun üzerinde gelir; bir nimf onu pelerinle bekler. O dönem Floransa’da alışılmadık biçimde tuvale yapılan eser, <b>Erken Rönesans</b>ın başyapıtlarındandır.'],
         fr: ['Voici <b>La Naissance de Vénus</b> de Sandro Botticelli.', 'La déesse arrive sur une coquille poussée par les vents, accueillie par une nymphe qui tend un manteau. Peinte sur toile, chose rare à Florence à l’époque, c’est un sommet de la <b>première Renaissance</b>.'],
         de: ['Das ist <b>Die Geburt der Venus</b> von Sandro Botticelli.', 'Die Göttin landet auf einer Muschel, von den Winden ans Ufer getrieben, eine Nymphe wartet mit einem Mantel. Auf Leinwand gemalt, damals in Florenz ungewöhnlich, ist sie ein Höhepunkt der <b>Frührenaissance</b>.'],
         es: ['Es <b>El nacimiento de Venus</b> de Sandro Botticelli.', 'La diosa llega sobre una concha, empujada a la orilla por los vientos, mientras una ninfa la espera con un manto. Pintada sobre lienzo, algo inusual en la Florencia de entonces, es una cumbre del <b>Primer Renacimiento</b>.'] } },
];

const pick = (v, lang) => (typeof v === 'string' ? v : v[lang]);
const dataUrl = f => 'data:image/' + (f.endsWith('.png') ? 'png' : 'webp') + ';base64,' + fs.readFileSync(f).toString('base64');

(async () => {
  const b = await chromium.launch({ channel: process.env.PW_CHANNEL || undefined });
  const p = await b.newPage({ viewport: { width: 393, height: 852 }, deviceScaleFactor: 3 });
  await p.goto('file://' + path.join(__dirname, 'screens.html'));
  const avatar = dataUrl(path.join(__dirname, 'avatar.png'));
  for (const lang of Object.keys(UI)) {
    for (let i = 0; i < SCENES.length; i++) {
      const s = SCENES[i], [close, title, ph, q] = UI[lang], lab = L[lang];
      const kv = s.kv.map(v => pick(v, lang));
      const [intro, story] = s.t[lang];
      const answer = `<p>${intro}</p><p class="kv"><b>${lab[0]}:</b> ${kv[0]}<br><b>${lab[1]}:</b> ${kv[1]}<br><b>${lab[2]}:</b> ${kv[2]}<br><b>${lab[3]}:</b> ${kv[3]}</p><p>${story}</p>`;
      await p.evaluate(({ close, title, ph, q, answer, photo, pos, avatar }) => {
        document.getElementById('close').textContent = close; document.getElementById('title').textContent = title;
        document.getElementById('ph').textContent = ph; document.getElementById('q').textContent = q;
        document.getElementById('a').innerHTML = answer;
        const im = document.getElementById('photo'); im.src = photo; im.style.objectPosition = pos;
        document.getElementById('avatar').src = avatar;
      }, { close, title, ph, q, answer, photo: dataUrl(path.join(ROOT, 'assets/art', s.img + '.webp')), pos: s.pos, avatar });
      await p.waitForTimeout(150);
      const png = path.join(require('os').tmpdir(), `screen-${lang}-${i + 1}.png`);
      await p.screenshot({ path: png });
      execFileSync('cwebp', ['-quiet', '-q', '82', '-resize', '645', '0', png, '-o', path.join(ROOT, 'assets/img', `screen-${lang}-${i + 1}.webp`)]);
      const overflow = await p.evaluate(() => document.querySelector('.bot .b').getBoundingClientRect().bottom > document.querySelector('.input').getBoundingClientRect().top - 8);
      console.log(lang, i + 1, overflow ? 'TEXT OVERFLOWS INPUT BAR' : 'ok');
    }
  }
  await b.close();
})();
