const styles = {
  'default': 'outputs/all_presets/default.json',
  'minimal': 'outputs/all_presets/minimal.json',
  'macao': 'outputs/all_presets/macao.json',
  'barcelona': 'outputs/all_presets/barcelona.json',
  'barcelona-plotter': 'outputs/all_presets/barcelona-plotter.json',
  'tijuca': 'outputs/all_presets/tijuca.json',
  'cb-bf-f': 'outputs/all_presets/cb-bf-f.json',
  'abraca-redencao': 'outputs/all_presets/abraca-redencao.json',
  'heerhugowaard': 'outputs/all_presets/heerhugowaard.json',
  'plotter': 'outputs/all_presets/plotter.json',
  'le-shine': 'outputs/all_presets/le-shine.json',
  'ukiyoe': 'outputs/all_presets/ukiyoe.json'
};

const places = [
  {
    id: 'stad-default',
    name: 'Stad van de Zon',
    location: 'Heerhugowaard, Netherlands',
    source: "prettymaps.plot('Stad van de Zon, Heerhugowaard, Netherlands')",
    center: [4.8249, 52.6496],
    zoom: 14.1,
    bearing: -8,
    pitch: 0,
    style: 'default',
    note: 'The circular Dutch solar-city example used at the start of the notebook.'
  },
  {
    id: 'stad-minimal',
    name: 'Stad van de Zon, minimal preset',
    location: 'Heerhugowaard, Netherlands',
    source: "preset = 'minimal'",
    center: [4.8249, 52.6496],
    zoom: 14.25,
    bearing: -8,
    pitch: 0,
    style: 'minimal',
    note: 'The same location, shown with the sparse minimal theme.'
  },
  {
    id: 'macau',
    name: 'Praça Ferreira do Amaral',
    location: 'Macau',
    source: "custom Macau example; converted with the macao preset",
    center: [113.5523, 22.1902],
    zoom: 15.3,
    bearing: 18,
    pitch: 0,
    style: 'macao',
    note: 'A compact urban-waterfront roundabout from the prettymaps examples.'
  },
  {
    id: 'bomfim',
    name: 'Bom Fim',
    location: 'Porto Alegre, Brazil',
    source: "prettymaps.plot('Bom Fim, Porto Alegre, Brasil')",
    center: [-51.2140, -30.0333],
    zoom: 14.4,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'A neighbourhood example with a larger non-circular extent in the notebook.'
  },
  {
    id: 'centro-historico',
    name: 'Centro Histórico',
    location: 'Porto Alegre, Brazil',
    source: "prettymaps.plot('Centro Histórico, Porto Alegre')",
    center: [-51.2304, -30.0325],
    zoom: 14.3,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'Used in the notebook for inspecting building GeoDataFrames.'
  },
  {
    id: 'barcelona',
    name: 'Eixample / Sagrada Família area',
    location: 'Barcelona, Spain',
    source: "prettymaps.plot((41.39491, 2.17557), preset = 'barcelona')",
    center: [2.17557, 41.39491],
    zoom: 15.1,
    bearing: -29,
    pitch: 0,
    style: 'barcelona',
    note: 'The gridded Barcelona showcase used for the Barcelona preset.'
  },
  {
    id: 'barcelona-plotter',
    name: 'Barcelona plotter variant',
    location: 'Barcelona, Spain',
    source: "preset = 'barcelona-plotter'",
    center: [2.17557, 41.39491],
    zoom: 15.1,
    bearing: -29,
    pitch: 0,
    style: 'barcelona-plotter',
    note: 'A line-art oriented variation of the Barcelona example.'
  },
  {
    id: 'tijuca',
    name: 'Barra da Tijuca',
    location: 'Rio de Janeiro, Brazil',
    source: "prettymaps.plot('Barra da Tijuca', preset = 'tijuca')",
    center: [-43.3650, -23.0004],
    zoom: 12.8,
    bearing: 0,
    pitch: 0,
    style: 'tijuca',
    note: 'A wide coastal and lagoon example from the notebook.'
  },
  {
    id: 'cidade-baixa',
    name: 'Cidade Baixa',
    location: 'Porto Alegre, Brazil',
    source: "prettymaps.Subplot('Cidade Baixa, Porto Alegre')",
    center: [-51.2228, -30.0392],
    zoom: 14.8,
    bearing: 0,
    pitch: 0,
    style: 'cb-bf-f',
    note: 'One of the three Porto Alegre neighbourhoods in the multiplot example.'
  },
  {
    id: 'farroupilha',
    name: 'Farroupilha',
    location: 'Porto Alegre, Brazil',
    source: "prettymaps.Subplot('Farroupilha, Porto Alegre')",
    center: [-51.2148, -30.0367],
    zoom: 14.8,
    bearing: 0,
    pitch: 0,
    style: 'cb-bf-f',
    note: 'Another neighbourhood from the Porto Alegre multiplot example.'
  },
  {
    id: 'honolulu',
    name: 'Honolulu',
    location: 'Hawaii, United States',
    source: "prettymaps.plot('Honolulu', radius = 5500)",
    center: [-157.8583, 21.3069],
    zoom: 12.2,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'The notebook uses this for hillshade experimentation; here it is shown with vector styling only.'
  },
  {
    id: 'garopaba',
    name: 'Garopaba',
    location: 'Santa Catarina, Brazil',
    source: "prettymaps.plot('Garopaba', radius = 5000)",
    center: [-48.6126, -28.0275],
    zoom: 12.8,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'A coastal keypoints example from the notebook; rendered here as an OpenFreeMap vector map.'
  },
  {
    id: 'le-shine-paris',
    name: 'Lè Shine blue-globe style',
    location: 'Paris, France',
    source: "Mapbox Lè Shine article-inspired special style",
    center: [2.3522, 48.8566],
    zoom: 12.8,
    bearing: -20,
    pitch: 0,
    style: 'le-shine',
    note: 'A standalone blue, globe-inspired MapLibre style with subtle dotted polygon texture; shown over Paris as the home of Lè Shine.'
  },
  {
    id: 'ukiyoe-museum-matsumoto',
    name: 'Ukiyo-e woodblock style',
    location: 'Japan Ukiyo-e Museum, Matsumoto, Japan',
    source: 'Japanese woodblock-print inspired special style',
    center: [137.9351, 36.2303],
    zoom: 14.2,
    bearing: -18,
    pitch: 0,
    style: 'ukiyoe',
    note: 'A standalone washi-paper, Prussian-blue, indigo, and vermilion MapLibre style with wave and hatch sprite textures; shown at the Japan Ukiyo-e Museum.'
  },
  {
    id: 'harekaer',
    name: 'Haveforeningen Harekær',
    location: 'Copenhagen, Denmark',
    source: "prettymaps.plot('Haveforeningen Harekær, Copenhagen')",
    center: [12.3982, 55.6365],
    zoom: 16.0,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'A garden allotment community in the southern suburbs of Copenhagen.'
  },
  {
    id: 'palmanova',
    name: 'Palmanova',
    location: 'Province of Udine, Italy',
    source: "prettymaps.plot('Palmanova, Italy')",
    center: [13.3101, 45.9068],
    zoom: 14.8,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'A Renaissance star-fort city in Friuli Venezia Giulia, Italy, with a distinctive nine-sided polygonal layout.'
  },
  {
    id: 'bourtange',
    name: 'Bourtange Fortress Museum',
    location: 'Groningen, Netherlands',
    source: "prettymaps.plot('Bourtange, Netherlands')",
    center: [7.1897, 53.0086],
    zoom: 15.5,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'A restored Dutch star fort and village in Groningen, originally built during the Eighty Years\u2019 War.'
  },
  {
    id: 'palm-jebel-ali',
    name: 'Palm Jebel Ali',
    location: 'Dubai, United Arab Emirates',
    source: "prettymaps.plot('Palm Jebel Ali, Dubai')",
    center: [54.9870, 25.0134],
    zoom: 12.5,
    bearing: 0,
    pitch: 0,
    style: 'default',
    note: 'A massive palm-shaped artificial archipelago under development in Dubai, south of the original Palm Jumeirah.'
  }
];

const placeSelect = document.getElementById('placeSelect');
const styleSelect = document.getElementById('styleSelect');
const textureSelect = document.getElementById('textureSelect');
const cards = document.getElementById('cards');
let currentIndex = 0;
let currentStyle = places[0].style;
let currentTexture = 'halftone';

function styleUrl(styleKey) {
  if (currentTexture === 'halftone') {
    return styles[styleKey].replace('outputs/all_presets/', 'outputs/all_presets_halftone/');
  }
  return styles[styleKey];
}

async function styleForMapLibre(styleKey) {
  const url = styleUrl(styleKey);
  // For flat (non-@2x) styles we can pass the URL directly — sprites are resolved
  // by MapLibre from the style's sprite field. For halftone we need to resolve
  // the relative "sprite" URLs to absolute paths.
  if (currentTexture !== 'halftone') return url;

  const response = await fetch(url);
  if (!response.ok) throw new Error(`Unable to load style ${url}: ${response.status}`);
  const style = await response.json();
  const styleBase = new URL(url, window.location.href);

  if (Array.isArray(style.sprite)) {
    style.sprite = style.sprite.map((entry) => ({
      ...entry,
      url: new URL(entry.url, styleBase).href
    }));
  } else if (typeof style.sprite === 'string') {
    style.sprite = new URL(style.sprite, styleBase).href;
  }

  return style;
}

async function applyStyle(styleKey) {
  const nextStyle = await styleForMapLibre(styleKey);
  map.setStyle(nextStyle);
  // After setStyle() the image registry is cleared. Eagerly re-register
  // the halftone sprites so they're ready for first render.
  if (currentTexture === 'halftone') {
    ensureHalftoneSprites(map).catch(() => {});
  }
}

for (const [key] of Object.entries(styles)) {
  const option = document.createElement('option');
  option.value = key;
  option.textContent = key;
  styleSelect.appendChild(option);
}

places.forEach((place, index) => {
  const option = document.createElement('option');
  option.value = String(index);
  option.textContent = `${place.name} — ${place.location}`;
  placeSelect.appendChild(option);

  const card = document.createElement('article');
  card.className = 'card';
  card.dataset.index = String(index);
  card.innerHTML = `
    <div class="eyebrow">${place.style}</div>
    <div class="name">${place.name}</div>
    <div class="meta">${place.location}</div>
    <div class="tags"><span class="tag">zoom ${place.zoom}</span><span class="tag">${place.source}</span></div>
  `;
  card.addEventListener('click', () => goToPlace(index, true));
  cards.appendChild(card);
});

const markerEl = document.createElement('div');
markerEl.className = 'marker';

const popup = new maplibregl.Popup({ offset: 28, closeButton: false });
const marker = new maplibregl.Marker({ element: markerEl, anchor: 'bottom' })
  .setLngLat(places[0].center)
  .setPopup(popup);

// ---------------------------------------------------------------------------
// Halftone sprite pre-loader — ensures pattern images are always available
// even before the sprite sheet finishes loading.
// ---------------------------------------------------------------------------
let _halftonePreloadPromise = null;

/** Load the halftone sprite JSON + PNG (choosing @2x if needed). */
async function _loadHalftoneSpriteData() {
  const ratio = Math.min(devicePixelRatio, 2);
  const suffix = ratio >= 2 ? '@2x' : '';
  const baseUrl = new URL('assets/halftone-sprite' + suffix, window.location.href).href.replace(/\.[^/.]+$/, '');
  const jsonUrl = baseUrl + '.json';
  const pngUrl  = baseUrl + '.png';

  const [jsonResp, pngResp] = await Promise.all([
    fetch(jsonUrl),
    fetch(pngUrl),
  ]);
  if (!jsonResp.ok) throw new Error(`Failed to load halftone sprite JSON: ${jsonUrl}`);
  if (!pngResp.ok)   throw new Error(`Failed to load halftone sprite PNG: ${pngUrl}`);

  const json = await jsonResp.json();
  const blob = await pngResp.blob();
  const img  = await createImageBitmap(blob, { colorSpaceConversion: 'none' });

  return { json, img, baseUrl };
}

/** Extract a sub-image from a sprite sheet and register it with the map. */
function _registerSpriteImage(map, name, spriteJson, spriteImg) {
  if (map.hasImage(name)) return; // already registered
  const meta = spriteJson[name];
  if (!meta) {
    console.warn(`Halftone sprite entry "${name}" not found in JSON.`);
    return;
  }
  const { x, y, width, height, pixelRatio } = meta;
  const texW = width * pixelRatio;
  const texH = height * pixelRatio;
  const canvas = document.createElement('canvas');
  canvas.width  = texW;
  canvas.height = texH;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(spriteImg, x, y, texW, texH, 0, 0, texW, texH);
  const imageData = ctx.getImageData(0, 0, texW, texH);
  map.addImage(name, { width: texW, height: texH, data: imageData.data }, { pixelRatio });
}

/** Ensure all halftone pattern images are registered on the map. */
async function ensureHalftoneSprites(map) {
  if (!_halftonePreloadPromise) {
    _halftonePreloadPromise = _loadHalftoneSpriteData().catch(err => {
      _halftonePreloadPromise = null; // allow retry on next call
      throw err;
    });
  }
  const { json, img } = await _halftonePreloadPromise;
  for (const name of Object.keys(json)) {
    _registerSpriteImage(map, name, json, img);
  }
}

// ---------------------------------------------------------------------------
// Map setup
// ---------------------------------------------------------------------------

const map = new maplibregl.Map({
  container: 'map',
  style: styleUrl(places[0].style),
  center: places[0].center,
  zoom: places[0].zoom,
  bearing: places[0].bearing,
  pitch: places[0].pitch,
  hash: true,
  attributionControl: true
});

map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'top-right');
map.addControl(new maplibregl.ScaleControl({ maxWidth: 120, unit: 'metric' }), 'bottom-right');
marker.addTo(map);

// Pre-load halftone sprites eagerly on map load so they are ready for switching.
map.on('load', () => {
  ensureHalftoneSprites(map).catch(() => {});
  syncUI();
  popup.addTo(map);
});

// Listen for any missing pm-* images and provide them on the fly.
// This covers the race condition where layers render before sprites arrive.
map.on('styleimagemissing', (e) => {
  if (typeof e.id !== 'string' || !e.id.startsWith('pm-')) return;
  ensureHalftoneSprites(map).then(() => {
    if (!map.hasImage(e.id)) {
      console.warn(`Halftone image "${e.id}" still missing after pre-load.`);
    }
  }).catch(err => {
    console.warn(`Failed to load halftone sprite for missing image "${e.id}":`, err);
  });
});

function popupHtml(place) {
  return `<div class="popup-title">${place.name}</div><div class="popup-subtitle">${place.location}<br>${place.note}</div>`;
}

function syncUI() {
  const place = places[currentIndex];
  placeSelect.value = String(currentIndex);
  styleSelect.value = currentStyle;
  textureSelect.value = currentTexture;
  textureSelect.disabled = false;
  textureSelect.title = 'Switch between flat colors and halftone texture overlays.';
  document.querySelectorAll('.card').forEach((card) => {
    card.classList.toggle('active', Number(card.dataset.index) === currentIndex);
  });
  const active = document.querySelector('.card.active');
  if (active) active.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
  popup.setHTML(popupHtml(place));
  marker.setLngLat(place.center);
}

async function setStyle(styleKey) {
  if (!styles[styleKey] || styleKey === currentStyle) return;
  currentStyle = styleKey;
  await applyStyle(styleKey);
}

async function setTexture(textureKey) {
  if (!['flat', 'halftone'].includes(textureKey) || textureKey === currentTexture) return;
  currentTexture = textureKey;
  await applyStyle(currentStyle);
  syncUI();
}

async function goToPlace(index, usePlaceStyle = true) {
  currentIndex = (index + places.length) % places.length;
  const place = places[currentIndex];
  if (usePlaceStyle) await setStyle(place.style);
  map.flyTo({
    center: place.center,
    zoom: place.zoom,
    bearing: place.bearing,
    pitch: place.pitch,
    duration: 1450,
    essential: true
  });
  syncUI();
}

placeSelect.addEventListener('change', (event) => goToPlace(Number(event.target.value), true));
styleSelect.addEventListener('change', (event) => setStyle(event.target.value).catch(console.error));
textureSelect.addEventListener('change', (event) => setTexture(event.target.value).catch(console.error));
document.getElementById('prevBtn').addEventListener('click', () => goToPlace(currentIndex - 1, true));
document.getElementById('nextBtn').addEventListener('click', () => goToPlace(currentIndex + 1, true));

map.on('styledata', () => {
  syncUI();
});