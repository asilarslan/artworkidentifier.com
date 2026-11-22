# Text guides. Same "key" across languages = translations (hreflang). "img" = artwork key for the hero image.

GUIDES = []


def g(key, lang, path, title, desc, h1, intro, body, faq, img=None, shot=None):
    GUIDES.append(dict(key=key, lang=lang, path=path, title=title, desc=desc, h1=h1, intro=intro, body=body, faq=faq,
                       img=img, shot=shot))


# ---------------------------------------------------------------- identify a painting
g("identify", "en", "/guides/how-to-identify-a-painting/",
  "How to Identify a Painting: 7 Ways to Find the Artist and Title",
  "Found a painting and want to know what it is? Use reverse image search, the signature, labels on the back, style and an artwork identifier app. Step by step.",
  "How to identify a painting",
  "Whether it's a work in a museum, a print in a café or a painting you inherited, these seven steps — from quickest to most thorough — will usually tell you what it is and who made it.",
  """
<ol class="checks">
<li><b>Snap it with an artwork identifier app</b>For well-known works, a photo is enough: the app tells you the title, artist, date and the story. Hold the phone straight to the canvas and avoid glare.</li>
<li><b>Reverse image search</b>Upload the photo to Google Lens or Bing Visual Search. Crop out the frame and wall; famous works and prints usually show up in seconds.</li>
<li><b>Look for a signature</b>Check the lower corners first, then along the edges. Photograph it in raking light (a torch held at a low angle). Partial signatures can be matched against signature databases and auction records.</li>
<li><b>Turn it over</b>Gallery stickers, exhibition labels, framer's stamps, inventory numbers, canvas maker's stamps and handwritten titles are all clues. Photograph everything before removing anything.</li>
<li><b>Check whether it's a print</b>Under a magnifier, printed reproductions show a regular dot pattern. A real painting has raised brushstrokes and uneven texture.</li>
<li><b>Identify the style and period</b>Brushwork, palette and subject point to a movement and era, which narrows the search. Our <a href="/art-styles/">art styles guide</a> and <a href="/art-style-finder/">style finder</a> help.</li>
<li><b>Ask the experts</b>Museum curators, auction houses and art historians often answer enquiries with good photos of the front, back and signature.</li>
</ol>
<h2>Good photos make everything easier</h2>
<ul><li>Daylight, no flash, no filters.</li><li>The whole work straight on, plus close-ups of signature, texture and the back.</li><li>Include a ruler for scale if you're asking experts.</li></ul>
""",
  [("Can I identify a painting from a photo?", "Yes. For famous works and their reproductions, an app or reverse image search usually finds it immediately. Unknown works need the signature, the back and expert help."),
   ("How do I find out who painted a picture with no signature?", "Look at the back for labels, compare the style with known artists, and ask an auction house or museum. Many fine paintings are unsigned.")],
  img="mona-lisa", shot=1)

g("identify", "tr", "/tr/rehber/tablo-nasil-taninir/",
  "Tablo Nasıl Tanınır? Ressamını ve Adını Bulmanın 7 Yolu",
  "Bir tablonun ne olduğunu ve kimin yaptığını öğrenmek için: tersine görsel arama, imza, arka yüzdeki etiketler, üslup ve sanat eseri tanıma uygulaması.",
  "Bir tablo nasıl tanınır?",
  "Müzedeki bir eser, kafedeki bir baskı ya da size miras kalan bir tablo… Bu yedi adım, en hızlısından en kapsamlısına, genellikle ne olduğunu ve kimin yaptığını ortaya çıkarır.",
  """
<ol class="checks">
<li><b>Sanat eseri tanıma uygulamasıyla çekin</b>Bilinen eserlerde bir fotoğraf yeter: uygulama adı, sanatçıyı, tarihi ve hikâyeyi söyler. Telefonu tabloya paralel tutun, parlamadan kaçının.</li>
<li><b>Tersine görsel arama</b>Fotoğrafı Google Lens'e veya Bing Görsel Arama'ya yükleyin. Çerçeveyi ve duvarı kırpın; ünlü eserler ve baskılar genellikle saniyeler içinde çıkar.</li>
<li><b>İmzayı arayın</b>Önce alt köşelere, sonra kenarlara bakın. Fenerle yandan, alçak açıdan ışık tutarak fotoğraflayın. Kısmi imzalar imza veri tabanları ve müzayede kayıtlarıyla eşleştirilebilir.</li>
<li><b>Arkasını çevirin</b>Galeri etiketleri, sergi etiketleri, çerçeveci damgaları, envanter numaraları, tuval üreticisi damgaları ve el yazısı başlıklar ipucudur. Hiçbir şeyi sökmeden önce fotoğraflayın.</li>
<li><b>Baskı olup olmadığına bakın</b>Büyüteçle bakınca baskılarda düzenli nokta deseni görülür. Gerçek bir yağlı boyada kabarık fırça izleri ve düzensiz doku vardır.</li>
<li><b>Üslubu ve dönemi belirleyin</b>Fırça işçiliği, renkler ve konu bir akımı ve dönemi işaret eder, aramayı daraltır. <a href="/tr/sanat-akimlari/">Sanat akımları rehberimiz</a> ve <a href="/tr/sanat-akimi-bulucu/">akım bulucu</a> yardımcı olur.</li>
<li><b>Uzmanlara sorun</b>Müze küratörleri, müzayede evleri ve sanat tarihçileri; önün, arkanın ve imzanın iyi fotoğraflarıyla gelen sorulara çoğu zaman yanıt verir.</li>
</ol>
<h2>İyi fotoğraf her şeyi kolaylaştırır</h2>
<ul><li>Gün ışığı, flaş yok, filtre yok.</li><li>Eserin tamamı düz açıdan; imza, doku ve arka yüzün yakın planları.</li><li>Uzmana soracaksanız ölçek için bir cetvel ekleyin.</li></ul>
""",
  [("Fotoğraftan tablo tanınır mı?", "Evet. Ünlü eserler ve baskıları uygulama ya da tersine görsel aramayla hemen bulunur. Bilinmeyen eserler için imza, arka yüz ve uzman görüşü gerekir."),
   ("İmzasız bir tablonun ressamı nasıl bulunur?", "Arka yüzdeki etiketlere bakın, üslubu bilinen ressamlarla karşılaştırın ve bir müzayede evine ya da müzeye danışın. Birçok değerli tablo imzasızdır.")],
  img="mona-lisa", shot=1)

g("identify", "fr", "/fr/guides/identifier-un-tableau/",
  "Comment identifier un tableau : 7 méthodes pour trouver l'artiste",
  "Vous voulez savoir ce que représente un tableau et qui l'a peint ? Recherche d'image inversée, signature, étiquettes au dos, style et application d'identification.",
  "Comment identifier un tableau",
  "Œuvre de musée, reproduction dans un café ou tableau hérité : ces sept étapes, de la plus rapide à la plus poussée, permettent généralement de savoir de quoi il s'agit.",
  """
<ol class="checks">
<li><b>Photographiez-le avec une app d'identification</b>Pour les œuvres connues, une photo suffit : titre, artiste, date et histoire. Tenez le téléphone bien parallèle et évitez les reflets.</li>
<li><b>Recherche d'image inversée</b>Importez la photo dans Google Lens ou Bing. Recadrez sans le cadre ni le mur.</li>
<li><b>Cherchez la signature</b>Coins inférieurs d'abord, puis les bords. Éclairez en lumière rasante avec une lampe.</li>
<li><b>Retournez le tableau</b>Étiquettes de galerie ou d'exposition, cachets d'encadreur, numéros d'inventaire, tampons de fournisseur de toile : autant d'indices.</li>
<li><b>Vérifiez s'il s'agit d'une reproduction</b>À la loupe, une impression montre une trame de points régulière ; une peinture a du relief.</li>
<li><b>Identifiez le style et l'époque</b>Touche, palette et sujet orientent vers un mouvement. Voir notre <a href="/fr/styles-artistiques/">guide des styles</a>.</li>
<li><b>Demandez à des experts</b>Musées, maisons de ventes et historiens de l'art répondent souvent avec de bonnes photos du recto, du verso et de la signature.</li>
</ol>
""",
  [("Peut-on identifier un tableau à partir d'une photo ?", "Oui pour les œuvres célèbres et leurs reproductions. Pour une œuvre inconnue, il faut la signature, le verso et un avis d'expert.")],
  img="mona-lisa", shot=1)

g("identify", "de", "/de/ratgeber/gemaelde-erkennen/",
  "Gemälde erkennen: 7 Wege, Künstler und Titel herauszufinden",
  "Du willst wissen, welches Gemälde das ist und wer es gemalt hat? Bildersuche, Signatur, Etiketten auf der Rückseite, Stil und eine App zur Kunsterkennung.",
  "Wie erkenne ich ein Gemälde?",
  "Ob Werk im Museum, Druck im Café oder geerbtes Bild: Diese sieben Schritte, vom schnellsten zum gründlichsten, verraten meist, was es ist und von wem.",
  """
<ol class="checks">
<li><b>Mit einer Kunsterkennungs-App fotografieren</b>Bei bekannten Werken reicht ein Foto: Titel, Künstler, Jahr und Geschichte. Handy parallel halten, Spiegelungen vermeiden.</li>
<li><b>Umgekehrte Bildersuche</b>Foto bei Google Lens oder Bing hochladen, Rahmen und Wand wegschneiden.</li>
<li><b>Signatur suchen</b>Zuerst untere Ecken, dann Ränder. Mit einer Taschenlampe im Streiflicht fotografieren.</li>
<li><b>Rückseite ansehen</b>Galerie- und Ausstellungsetiketten, Rahmenmacherstempel, Inventarnummern und Leinwandstempel sind Hinweise.</li>
<li><b>Druck oder Gemälde?</b>Unter der Lupe zeigt ein Druck ein regelmäßiges Punktraster; ein Gemälde hat Pinselrelief.</li>
<li><b>Stil und Epoche bestimmen</b>Pinselstrich, Farben und Motiv grenzen die Suche ein. Siehe unseren <a href="/de/kunststile/">Kunststile-Ratgeber</a>.</li>
<li><b>Experten fragen</b>Museen, Auktionshäuser und Kunsthistoriker antworten oft auf Anfragen mit guten Fotos von Vorder-, Rückseite und Signatur.</li>
</ol>
""",
  [("Kann man ein Gemälde per Foto erkennen?", "Ja, berühmte Werke und Reproduktionen meist sofort. Unbekannte Werke brauchen Signatur, Rückseite und Expertenrat.")],
  img="mona-lisa", shot=1)

g("identify", "es", "/es/guias/como-identificar-un-cuadro/",
  "Cómo identificar un cuadro: 7 formas de encontrar el autor y el título",
  "¿Quieres saber qué cuadro es y quién lo pintó? Búsqueda inversa de imágenes, firma, etiquetas del reverso, estilo y una app para identificar obras de arte.",
  "Cómo identificar un cuadro",
  "Una obra en un museo, una lámina en un café o un cuadro heredado: estos siete pasos, del más rápido al más completo, suelen revelar qué es y quién lo hizo.",
  """
<ol class="checks">
<li><b>Fotografíalo con una app de identificación</b>Para obras conocidas basta una foto: título, artista, fecha e historia. Sostén el móvil paralelo y evita reflejos.</li>
<li><b>Búsqueda inversa de imágenes</b>Sube la foto a Google Lens o Bing y recorta el marco y la pared.</li>
<li><b>Busca la firma</b>Primero las esquinas inferiores, luego los bordes. Ilumina con una linterna en ángulo rasante.</li>
<li><b>Dale la vuelta</b>Etiquetas de galería o exposición, sellos del enmarcador, números de inventario y sellos del fabricante del lienzo son pistas.</li>
<li><b>¿Lámina o pintura?</b>Con lupa, una impresión muestra una trama de puntos regular; una pintura tiene relieve.</li>
<li><b>Identifica el estilo y la época</b>Pincelada, paleta y tema orientan la búsqueda. Mira nuestra <a href="/es/estilos-artisticos/">guía de estilos</a>.</li>
<li><b>Consulta a expertos</b>Museos, casas de subastas e historiadores del arte suelen responder si envías buenas fotos del anverso, el reverso y la firma.</li>
</ol>
""",
  [("¿Se puede identificar un cuadro con una foto?", "Sí, las obras famosas y sus reproducciones casi al instante. Una obra desconocida necesita la firma, el reverso y la opinión de un experto.")],
  img="mona-lisa", shot=1)

# ---------------------------------------------------------------- is my painting valuable
g("value", "en", "/guides/is-my-painting-valuable/",
  "Is My Painting Valuable? How to Find Out What It's Worth",
  "Think you have a valuable painting? Check if it's an original or a print, find the artist, look at auction records and get a professional appraisal. Honest step-by-step guide.",
  "Is my painting valuable?",
  "Most paintings found at home are prints or decorative works — but some turn out to be worth far more than expected. Here's how to tell which you have, without paying for an appraisal too early.",
  """
<h2>1. Original or reproduction?</h2>
<ul><li><b>Magnifier test:</b> a regular dot pattern means a printed reproduction.</li><li><b>Texture:</b> an oil painting has raised brushstrokes; a print on canvas is usually flat, sometimes with clear varnish strokes added on top.</li><li><b>Edges:</b> on a real painting the paint often stops unevenly at the edges of the canvas.</li><li><b>Limited-edition prints</b> are usually numbered (e.g. 23/100) and signed in pencil, and can still have value.</li></ul>
<h2>2. Who made it?</h2>
<p>Use our <a href="/guides/how-to-identify-a-painting/">guide to identifying a painting</a>: signature, labels on the back and style. A known artist name is the single biggest factor in value.</p>
<h2>3. Check auction records</h2>
<p>Search the artist's name on auction result databases and the online archives of major auction houses. Compare size, medium, period and condition, not just the name.</p>
<h2>4. What affects value</h2>
<ul><li>Artist and authenticity</li><li>Provenance: the documented history of ownership</li><li>Condition: tears, flaking paint, overpainting</li><li>Size, subject and period within the artist's career</li><li>Market demand right now</li></ul>
<h2>5. Get a professional appraisal</h2>
<p>For anything promising, contact a regional auction house (many give free initial opinions from photos) or an accredited appraiser. Be wary of anyone who offers to buy it on the spot.</p>
<div class="note-box">An app can tell you about the style and the artist it resembles, but it can't authenticate a painting or put a reliable price on it.</div>
""",
  [("How can I tell if a painting is an original?", "Look for brushstroke texture, uneven paint at the edges and the absence of a printed dot pattern under a magnifier."),
   ("Are unsigned paintings worthless?", "No. Many old paintings are unsigned. Style, quality, provenance and expert attribution matter more than a signature.")],
  img="the-lacemaker")

g("value", "tr", "/tr/rehber/tablo-degerli-mi/",
  "Tablom Değerli mi? Bir Tablonun Değeri Nasıl Anlaşılır?",
  "Evdeki tablonun değerli olup olmadığını anlamak için: orijinal mi baskı mı, ressamı kim, müzayede kayıtları ve profesyonel ekspertiz. Dürüst, adım adım rehber.",
  "Tablom değerli mi?",
  "Evde bulunan tabloların çoğu baskı ya da dekoratif eserdir; ama bazıları beklenenden çok daha değerli çıkar. Erkenden ekspertize para ödemeden hangisine sahip olduğunuzu anlamanın yolu şöyle.",
  """
<h2>1. Orijinal mi, baskı mı?</h2>
<ul><li><b>Büyüteç testi:</b> düzenli nokta deseni baskı demektir.</li><li><b>Doku:</b> yağlı boyada kabarık fırça izleri vardır; tuval baskılar genellikle düzdür, bazen üstüne şeffaf vernik darbeleri eklenir.</li><li><b>Kenarlar:</b> gerçek tabloda boya çoğu zaman tuvalin kenarında düzensiz biter.</li><li><b>Sınırlı sayıda baskılar</b> genellikle numaralıdır (ör. 23/100) ve kurşun kalemle imzalıdır; bunların da değeri olabilir.</li></ul>
<h2>2. Kim yaptı?</h2>
<p><a href="/tr/rehber/tablo-nasil-taninir/">Tablo nasıl tanınır rehberimizi</a> kullanın: imza, arka yüzdeki etiketler ve üslup. Bilinen bir sanatçı adı değeri en çok etkileyen faktördür.</p>
<h2>3. Müzayede kayıtlarına bakın</h2>
<p>Sanatçının adını müzayede sonuç veri tabanlarında ve büyük müzayede evlerinin çevrim içi arşivlerinde aratın. Yalnızca ada değil; boyuta, tekniğe, döneme ve duruma göre karşılaştırın.</p>
<h2>4. Değeri ne belirler?</h2>
<ul><li>Sanatçı ve orijinallik</li><li>Provenans: belgelenmiş sahiplik geçmişi</li><li>Durum: yırtık, dökülen boya, rötuş</li><li>Boyut, konu ve sanatçının kariyerindeki dönem</li><li>O anki piyasa talebi</li></ul>
<h2>5. Profesyonel ekspertiz</h2>
<p>Umut verici bir şey varsa bir müzayede evine (birçoğu fotoğraftan ücretsiz ön görüş verir) veya yetkili bir eksper başvurun. Hemen satın almayı teklif edenlere karşı dikkatli olun.</p>
<div class="note-box">Bir uygulama üslubu ve benzediği sanatçıyı söyleyebilir, ancak bir tablonun orijinalliğini kanıtlayamaz ya da güvenilir bir fiyat biçemez.</div>
""",
  [("Tablonun orijinal olduğu nasıl anlaşılır?", "Fırça dokusuna, kenarlarda düzensiz biten boyaya ve büyüteç altında baskı noktası olmamasına bakın."),
   ("İmzasız tablolar değersiz mi?", "Hayır. Birçok eski tablo imzasızdır. Üslup, kalite, provenans ve uzman atfı imzadan daha önemlidir.")],
  img="the-lacemaker")

# Art movements guide intros (body is generated from content.artworks.MOVEMENTS)
STYLES = {
    "en": dict(path="/art-styles/", title="Art Styles Guide: How to Recognise 16 Art Movements (with Examples)",
               desc="How to recognise art movements at a glance: Renaissance, Baroque, Impressionism, Post-Impressionism, Cubism, Expressionism, Surrealism, Pop Art and more, each with a famous example.",
               h1="How to recognise art styles", intro="Sixteen art movements, in order, with the clues that give each one away and a famous example you can see in a museum.",
               years="Years", clue="How to recognise it", example="Famous example"),
    "tr": dict(path="/tr/sanat-akimlari/", title="Sanat Akımları Rehberi: 16 Akım Nasıl Ayırt Edilir? (Örnekleriyle)",
               desc="Sanat akımlarını bir bakışta tanıyın: Rönesans, Barok, Empresyonizm, Post-Empresyonizm, Kübizm, Dışavurumculuk, Sürrealizm, Pop Art ve dahası; her biri ünlü bir örnekle.",
               h1="Sanat akımları nasıl ayırt edilir?", intro="Kronolojik sırayla 16 sanat akımı, her birini ele veren ipuçları ve müzede görebileceğiniz ünlü bir örnek.",
               years="Dönem", clue="Nasıl tanınır", example="Ünlü örnek"),
    "fr": dict(path="/fr/styles-artistiques/", title="Les mouvements artistiques : comment reconnaître 16 styles (avec exemples)",
               desc="Reconnaître les mouvements artistiques en un coup d'œil : Renaissance, baroque, impressionnisme, cubisme, expressionnisme, surréalisme, pop art… avec un exemple célèbre pour chacun.",
               h1="Comment reconnaître les styles artistiques", intro="Seize mouvements, dans l'ordre, avec les indices qui les trahissent et un exemple célèbre.",
               years="Période", clue="Comment le reconnaître", example="Exemple célèbre"),
    "de": dict(path="/de/kunststile/", title="Kunststile erkennen: 16 Kunstrichtungen mit Beispielen",
               desc="Kunstrichtungen auf einen Blick erkennen: Renaissance, Barock, Impressionismus, Kubismus, Expressionismus, Surrealismus, Pop-Art und mehr, jeweils mit einem berühmten Beispiel.",
               h1="Kunststile erkennen", intro="Sechzehn Kunstrichtungen in zeitlicher Folge, mit den typischen Merkmalen und einem berühmten Beispiel.",
               years="Zeitraum", clue="Woran man ihn erkennt", example="Berühmtes Beispiel"),
    "es": dict(path="/es/estilos-artisticos/", title="Estilos artísticos: cómo reconocer 16 movimientos (con ejemplos)",
               desc="Reconoce los movimientos artísticos de un vistazo: Renacimiento, Barroco, Impresionismo, Cubismo, Expresionismo, Surrealismo, arte pop y más, cada uno con un ejemplo famoso.",
               h1="Cómo reconocer los estilos artísticos", intro="Dieciséis movimientos en orden, con las pistas que los delatan y un ejemplo famoso.",
               years="Época", clue="Cómo reconocerlo", example="Ejemplo famoso"),
}

MUSEUM_HUBS = {
    "en": dict(path="/museums/", title="Museum Guides: Must-See Artworks at the World's Great Museums",
               desc="What to see first at the Louvre, Musée d'Orsay, the Met, Uffizi, Rijksmuseum, Prado, National Gallery and Vatican Museums — with images and visit tips.",
               h1="Museum guides", intro="The artworks not to miss at the world's great museums, with what to look for and practical tips."),
    "tr": dict(path="/tr/muzeler/", title="Müze Rehberleri: Dünyanın Büyük Müzelerinde Görülmesi Gereken Eserler",
               desc="Louvre ve dünyanın büyük müzelerinde önce neler görülmeli? Görseller, neye bakmalı ve ziyaret ipuçları.",
               h1="Müze rehberleri", intro="Dünyanın büyük müzelerinde kaçırılmaması gereken eserler."),
    "fr": dict(path="/fr/musees/", title="Guides de musées : les œuvres incontournables",
               desc="Que voir en premier au Louvre et au musée d'Orsay ? Les œuvres, ce qu'il faut observer et nos conseils.",
               h1="Guides de musées", intro="Les œuvres à ne pas manquer dans les grands musées."),
    "de": dict(path="/de/museen/", title="Museumsführer: Die wichtigsten Kunstwerke",
               desc="Was du im Rijksmuseum und in den großen Museen der Welt zuerst sehen solltest, mit Bildern und Tipps.",
               h1="Museumsführer", intro="Die Werke, die du in den großen Museen nicht verpassen solltest."),
    "es": dict(path="/es/museos/", title="Guías de museos: las obras imprescindibles",
               desc="Qué ver primero en el Museo del Prado y otros grandes museos, con imágenes y consejos.",
               h1="Guías de museos", intro="Las obras que no te puedes perder en los grandes museos."),
}
