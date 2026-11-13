(() => {
  'use strict';

  const NIVEAUX = ['critique', 'eleve', 'moyen', 'info'];
  const CATEGORIES = { backdoor: 'backdoor', syntaxe: 'syntaxe', manifeste: 'manifeste', config: 'manifeste' };

  const T = {
    fr: {
      langue: 'Langue',
      chapo: 'Passe ton serveur FiveM aux rayons X : backdoors, code caché et erreurs de syntaxe, en quelques secondes et sans rien envoyer sur internet.',
      v_backdoors_t: 'Backdoors',
      v_backdoors: 'Code téléchargé puis exécuté, texte caché, vol de la clé serveur, droits admin donnés en douce, infection des autres ressources.',
      v_syntaxe_t: 'Syntaxe',
      v_syntaxe: 'Chaque fichier Lua passe dans le vrai compilateur Lua 5.4, chaque JSON est relu.',
      v_manifestes_t: 'Manifestes',
      v_manifestes: 'Fichiers déclarés introuvables, ressources en double, ensure vers des ressources absentes.',
      choisir_aria: 'Choisir le dossier du serveur',
      depot_titre: 'Glisse ici le dossier de ton serveur',
      depot_aide: 'Le dossier qui contient server.cfg, ou directement resources',
      choisir: 'Choisir un dossier',
      recents: 'Analysés récemment',
      lecture: 'Lecture du dossier…',
      analyse_de: (n) => `Analyse de ${pl(n, 'ressource', 'ressources')}`,
      fichiers_sur: (a, b) => `${nf(a)} / ${nf(b)} fichiers`,
      arreter: 'Arrêter',
      arret: 'Arrêt…',
      nouvelle: 'Nouvelle analyse',
      relancer: 'Relancer',
      exporter: 'Exporter le rapport',
      filtrer: 'Filtrer par gravité',
      ressources: 'Ressources',
      toutes: 'Toutes',
      tab_tout: 'Tout',
      tab_backdoors: 'Backdoors',
      tab_syntaxe: 'Syntaxe',
      tab_manifestes: 'Manifestes et config',
      chercher: 'Chercher un fichier, une ressource…',
      niveaux: { critique: 'Critique', eleve: 'Élevé', moyen: 'Moyen', info: 'Info' },
      masquer: (n) => `Masquer le niveau ${n}`,
      afficher: (n) => `Afficher le niveau ${n}`,
      v_critique: 'Backdoor probable',
      v_critique_d: (n) => `${pl(n, 'problème critique', 'problèmes critiques')}. Ne lance pas ces ressources avant d'avoir vérifié.`,
      v_eleve: 'Des points à vérifier',
      v_eleve_d: (n) => `${pl(n, 'élément de code sensible', 'éléments de code sensibles')}, sans signe clair de backdoor.`,
      v_sain: 'Aucune backdoor trouvée',
      v_sain_syntaxe: (n) => `${pl(n, 'erreur de syntaxe', 'erreurs de syntaxe')} à corriger.`,
      v_sain_rien: 'Aucune erreur de syntaxe non plus.',
      interrompu: ' Analyse arrêtée avant la fin.',
      stats: (s, d, v) => `${pl(s.fichiers, 'fichier lu', 'fichiers lus')}, ${pl(s.lignes, 'ligne', 'lignes')}, ${pl(s.ressources, 'ressource', 'ressources')} en ${d} s. Nemesys Scanner ${v}.`,
      hors_ressource: '(hors ressource)',
      probleme: (n) => pl(n, 'problème', 'problèmes'),
      rien_trouve: 'rien trouvé',
      escrow: ' (protégée par Escrow)',
      legende: 'Une case par ressource. Clique pour filtrer.',
      filtre_sur: (r) => `Filtré sur ${r}`,
      vide_rien: 'Rien à signaler',
      vide_rien_d: 'Aucune backdoor, aucune erreur de syntaxe.',
      vide_filtre: 'Aucun problème avec ces filtres',
      vide_filtre_d: 'Réactive un niveau de gravité ou change d\'onglet.',
      detail_vide: 'Choisis un problème dans la liste pour voir le code concerné et quoi faire.',
      syntaxe: 'syntaxe',
      ligne: (n) => ` : ligne ${n}`,
      message_lua: (m) => `Message Lua d'origine : ${m}`,
      decode: 'Ce que le texte caché contient vraiment',
      autres: (n) => `Et ${pl(n, 'autre fois', 'autres fois')} dans ce même fichier.`,
      que_faire: 'Que faire',
      ouvrir: 'Ouvrir dans l\'éditeur',
      ouvrir_ko: 'Impossible d\'ouvrir le fichier.',
      copier: 'Copier le chemin',
      copie_ok: 'Chemin copié',
      copie_ko: 'Copie impossible',
      ignorer: 'Ignorer',
      ignorer_t: 'Masquer ce problème dans les prochaines analyses',
      ignore_ok: 'Problème ignoré',
      dossier_ko: 'Impossible de lire ce dossier.',
    },
    en: {
      langue: 'Language',
      chapo: 'X-ray your FiveM server: backdoors, hidden code and syntax errors, in seconds and without sending anything online.',
      v_backdoors_t: 'Backdoors',
      v_backdoors: 'Code downloaded then executed, hidden strings, server key theft, sneaky admin rights, resources infecting each other.',
      v_syntaxe_t: 'Syntax',
      v_syntaxe: 'Every Lua file goes through the real Lua 5.4 compiler, every JSON file is parsed.',
      v_manifestes_t: 'Manifests',
      v_manifestes: 'Declared files that don\'t exist, duplicate resources, ensure lines pointing to missing resources.',
      choisir_aria: 'Choose the server folder',
      depot_titre: 'Drop your server folder here',
      depot_aide: 'The folder that contains server.cfg, or the resources folder itself',
      choisir: 'Choose a folder',
      recents: 'Recently scanned',
      lecture: 'Reading the folder…',
      analyse_de: (n) => `Scanning ${pl(n, 'resource', 'resources')}`,
      fichiers_sur: (a, b) => `${nf(a)} / ${nf(b)} files`,
      arreter: 'Stop',
      arret: 'Stopping…',
      nouvelle: 'New scan',
      relancer: 'Scan again',
      exporter: 'Export report',
      filtrer: 'Filter by severity',
      ressources: 'Resources',
      toutes: 'All',
      tab_tout: 'All',
      tab_backdoors: 'Backdoors',
      tab_syntaxe: 'Syntax',
      tab_manifestes: 'Manifests and config',
      chercher: 'Search a file or resource…',
      niveaux: { critique: 'Critical', eleve: 'High', moyen: 'Medium', info: 'Info' },
      masquer: (n) => `Hide ${n} findings`,
      afficher: (n) => `Show ${n} findings`,
      v_critique: 'Likely backdoor',
      v_critique_d: (n) => `${pl(n, 'critical finding', 'critical findings')}. Don't start these resources before checking them.`,
      v_eleve: 'A few things to check',
      v_eleve_d: (n) => `${pl(n, 'sensitive piece of code', 'sensitive pieces of code')}, with no clear sign of a backdoor.`,
      v_sain: 'No backdoor found',
      v_sain_syntaxe: (n) => `${pl(n, 'syntax error', 'syntax errors')} to fix.`,
      v_sain_rien: 'No syntax errors either.',
      interrompu: ' Scan stopped before the end.',
      stats: (s, d, v) => `${pl(s.fichiers, 'file read', 'files read')}, ${pl(s.lignes, 'line', 'lines')}, ${pl(s.ressources, 'resource', 'resources')} in ${d} s. Nemesys Scanner ${v}.`,
      hors_ressource: '(outside resources)',
      probleme: (n) => pl(n, 'finding', 'findings'),
      rien_trouve: 'nothing found',
      escrow: ' (Escrow protected)',
      legende: 'One square per resource. Click to filter.',
      filtre_sur: (r) => `Filtered on ${r}`,
      vide_rien: 'Nothing to report',
      vide_rien_d: 'No backdoor, no syntax error.',
      vide_filtre: 'No findings with these filters',
      vide_filtre_d: 'Turn a severity level back on or switch tabs.',
      detail_vide: 'Pick a finding in the list to see the code involved and what to do.',
      syntaxe: 'syntax',
      ligne: (n) => `: line ${n}`,
      message_lua: () => '',
      decode: 'What the hidden text really contains',
      autres: (n) => `And ${pl(n, 'more time', 'more times')} in this same file.`,
      que_faire: 'What to do',
      ouvrir: 'Open in editor',
      ouvrir_ko: 'Could not open the file.',
      copier: 'Copy path',
      copie_ok: 'Path copied',
      copie_ko: 'Copy failed',
      ignorer: 'Ignore',
      ignorer_t: 'Hide this finding in future scans',
      ignore_ok: 'Finding ignored',
      dossier_ko: 'Could not read this folder.',
    },
  };

  const $ = (s) => document.getElementById(s);
  const app = $('app');
  const integre = window.RAPPORT_INTEGRE || null;

  const etat = {
    rapport: null,
    dossier: '',
    langue: 'fr',
    niveaux: new Set(['critique', 'eleve', 'moyen']),
    categorie: 'tout',
    ressource: null,
    recherche: '',
    choisi: null,
    visibles: [],
    ignores: new Set(lireStockage('ns-ignores', [])),
    cases: new Map(),
  };

  function lireStockage(cle, defaut) {
    try { const v = localStorage.getItem(cle); return v ? JSON.parse(v) : defaut; } catch { return defaut; }
  }
  function ecrireStockage(cle, valeur) {
    try { localStorage.setItem(cle, JSON.stringify(valeur)); } catch {                             }
  }
  const t = (cle, ...a) => { const v = T[etat.langue][cle]; return typeof v === 'function' ? v(...a) : v; };
  const nf = (n) => n.toLocaleString(etat.langue === 'fr' ? 'fr-FR' : 'en-US');
  const pl = (n, un, plusieurs) => `${nf(n)} ${n > 1 ? plusieurs : un}`;
  const nomNiveau = (n) => T[etat.langue].niveaux[n];
  const tp = (p, champ) => (etat.langue === 'en' && p.en ? p.en[champ] : p[champ]);
  const nomRessource = (r) => (r === '(hors ressource)' ? t('hors_ressource') : r);

  function el(tag, attrs = {}, ...enfants) {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v === undefined || v === null || v === false) continue;
      if (k === 'class') n.className = v;
      else if (k === 'text') n.textContent = v;
      else if (k.startsWith('on')) n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v === true ? '' : v);
    }
    for (const e of enfants.flat()) if (e !== null && e !== undefined && e !== false) n.append(e);
    return n;
  }
  const api = () => (window.pywebview && window.pywebview.api) || null;
  const cleIgnore = (p) => `${p.regle}|${p.fichier}|${p.ligne || 0}`;

  let minuteurToast;
  function toast(msg) {
    const z = $('toast');
    z.textContent = msg; z.hidden = false;
    clearTimeout(minuteurToast);
    minuteurToast = setTimeout(() => { z.hidden = true; }, 2600);
  }
  const ecran = (nom) => { app.dataset.ecran = nom; };

  function langueInitiale() {
    const memo = lireStockage('ns-langue', null);
    if (memo === 'fr' || memo === 'en') return memo;
    return (navigator.language || 'en').toLowerCase().startsWith('fr') ? 'fr' : 'en';
  }

  function appliquerLangue(langue) {
    etat.langue = langue;
    document.documentElement.lang = langue;
    for (const n of document.querySelectorAll('[data-i18n]')) n.textContent = t(n.dataset.i18n);
    for (const n of document.querySelectorAll('[data-i18n-placeholder]')) n.placeholder = t(n.dataset.i18nPlaceholder);
    for (const n of document.querySelectorAll('[data-i18n-aria]')) n.setAttribute('aria-label', t(n.dataset.i18nAria));
    for (const zone of document.querySelectorAll('.langues')) {
      zone.replaceChildren(...['fr', 'en'].map((l) => el('button', {
        text: l.toUpperCase(), lang: l, 'aria-pressed': String(l === langue),
        title: l === 'fr' ? 'Français' : 'English',
        onclick: () => { ecrireStockage('ns-langue', l); appliquerLangue(l); },
      })));
    }
    if (app.dataset.ecran === 'analyse' && !etat.cases.size) $('analyse-titre').textContent = t('lecture');
    if (app.dataset.ecran === 'analyse' && etat.cases.size) $('analyse-titre').textContent = t('analyse_de', etat.cases.size);
    if (etat.rapport) {
      remplirVerdict();
      construireFiltres();
      construireRadio();
      rendreListe();
      const p = etat.rapport.problemes.find((x) => x.id === etat.choisi);
      rendreDetail(p || null);
    } else {
      rendreDetail(null);
    }
  }

  function decorDepot() {
    const g = document.querySelector('.depot-grille');
    const frag = document.createDocumentFragment();
    for (let i = 0; i < 260; i++) {
      const r = Math.random();
      frag.append(el('i', { class: r > .93 ? 'v' : r > .7 ? 'l' : '' }));
    }
    g.append(frag);
  }

  function afficherRecents() {
    const recents = lireStockage('ns-recents', []);
    const ul = $('liste-recents');
    ul.replaceChildren();
    $('recents').hidden = !recents.length;
    for (const d of recents) {
      ul.append(el('li', {}, el('button', { text: d, title: d, onclick: () => lancer(d) })));
    }
  }
  function memoriserRecent(d) {
    const recents = lireStockage('ns-recents', []).filter((x) => x !== d);
    recents.unshift(d);
    ecrireStockage('ns-recents', recents.slice(0, 6));
  }

  async function choisir() {
    const a = api();
    if (!a) return;
    const d = await a.choisir_dossier();
    if (d) lancer(d);
  }

  let derniereCase = null;

  async function lancer(dossier) {
    const a = api();
    if (!a) return;
    etat.dossier = dossier;
    etat.cases.clear();
    derniereCase = null;
    $('radio-analyse').replaceChildren();
    $('analyse-titre').textContent = t('lecture');
    $('analyse-dossier').textContent = dossier;
    $('analyse-compte').textContent = '';
    $('analyse-fichier').textContent = '';
    $('jauge').style.width = '0';
    ecran('analyse');
    memoriserRecent(dossier);
    const ok = await a.lancer(dossier, etat.langue);
    if (ok !== true) {
      ecran('accueil');
      toast(ok || t('dossier_ko'));
    }
  }

  function trouverCase(chemin) {
    let meilleure = null;
    let longueur = -1;
    for (const [prefixe, c] of etat.cases) {
      if ((chemin === prefixe || chemin.startsWith(prefixe + '/')) && prefixe.length > longueur) {
        meilleure = c; longueur = prefixe.length;
      }
    }
    return meilleure;
  }

  window.NS = {
    progres(p) {
      if (p.phase === 'ressources') {
        const radio = $('radio-analyse');
        const frag = document.createDocumentFragment();
        for (const r of p.info) {
          const c = el('div', { class: 'case', title: r.nom });
          etat.cases.set(r.chemin, c);
          frag.append(c);
        }
        radio.append(frag);
        $('analyse-titre').textContent = t('analyse_de', p.info.length);
        return;
      }
      if (p.phase !== 'analyse') return;
      $('jauge').style.width = `${Math.min(100, (p.fait / Math.max(1, p.total)) * 100)}%`;
      $('analyse-compte').textContent = t('fichiers_sur', p.fait, p.total);
      $('analyse-fichier').textContent = p.info;
      const c = trouverCase(p.info);
      if (c && c !== derniereCase) {
        if (derniereCase) { derniereCase.classList.remove('en-cours'); derniereCase.classList.add('lue'); }
        c.classList.add('en-cours');
        derniereCase = c;
      }
    },
    async fini() {
      const rapport = await api().resultat();
      montrerResultats(rapport);
    },
    erreur(message) {
      ecran('accueil');
      toast(message);
    },
    deposer(dossier) { lancer(dossier); },
  };

  function pireNiveau(liste) {
    for (const n of NIVEAUX) if (liste.some((p) => p.niveau === n)) return n;
    return null;
  }

  function remplirVerdict() {
    const rapport = etat.rapport;
    const quand = new Date(rapport.date);
    const date = Number.isNaN(quand.getTime()) ? rapport.date
      : quand.toLocaleString(etat.langue === 'fr' ? 'fr-FR' : 'en-GB', { dateStyle: 'medium', timeStyle: 'short' });
    $('r-dossier').textContent = `${rapport.racine} · ${date}`;
    $('r-dossier').title = rapport.racine;
    const nb = (n) => rapport.problemes.filter((p) => p.niveau === n && p.categorie === 'backdoor').length;
    const syntaxe = rapport.problemes.filter((p) => p.categorie === 'syntaxe').length;
    let titre; let detail;
    if (nb('critique')) { titre = t('v_critique'); detail = t('v_critique_d', nb('critique')); }
    else if (nb('eleve')) { titre = t('v_eleve'); detail = t('v_eleve_d', nb('eleve')); }
    else { titre = t('v_sain'); detail = syntaxe ? t('v_sain_syntaxe', syntaxe) : t('v_sain_rien'); }
    if (rapport.interrompu) detail += t('interrompu');
    $('verdict-titre').textContent = titre;
    $('verdict-detail').textContent = detail;
    const duree = String(rapport.duree).replace('.', etat.langue === 'fr' ? ',' : '.');
    $('stats').textContent = t('stats', rapport.stats, duree, rapport.version);
  }

  function montrerResultats(rapport) {
    etat.rapport = rapport;
    etat.ressource = null;
    etat.choisi = null;
    etat.recherche = '';
    $('recherche').value = '';
    ecran('resultats');

    const s = rapport.score;
    const trait = $('note-trait');
    trait.style.stroke = s >= 85 ? 'var(--sain)' : s >= 60 ? 'var(--moyen)' : s >= 36 ? 'var(--eleve)' : 'var(--critique)';
    requestAnimationFrame(() => { trait.style.strokeDashoffset = String(326.7 * (1 - s / 100)); });
    $('note-valeur').textContent = s;

    remplirVerdict();
    construireFiltres();
    construireRadio();
    rendreListe();
    rendreDetail(null);
  }

  function construireFiltres() {
    const zone = $('filtres-niveaux');
    zone.replaceChildren();
    for (const n of NIVEAUX) {
      const total = etat.rapport.problemes.filter((p) => p.niveau === n && !etat.ignores.has(cleIgnore(p))).length;
      zone.append(el('button', {
        class: 'filtre-niveau', 'data-niveau': n, 'aria-pressed': String(etat.niveaux.has(n)),
        title: etat.niveaux.has(n) ? t('masquer', nomNiveau(n)) : t('afficher', nomNiveau(n)),
        onclick: () => {
          if (etat.niveaux.has(n)) etat.niveaux.delete(n); else etat.niveaux.add(n);
          construireFiltres(); rendreListe();
        },
      }, el('span', { class: 'pastille', text: nomNiveau(n) }), el('b', { text: total })));
    }
  }

  function construireRadio() {
    const radio = $('radio-resultats');
    radio.replaceChildren();
    radio.classList.toggle('filtre', !!etat.ressource);
    $('tout-voir').hidden = !etat.ressource;
    const parRes = new Map();
    for (const p of etat.rapport.problemes) {
      if (etat.ignores.has(cleIgnore(p))) continue;
      if (!parRes.has(p.ressource)) parRes.set(p.ressource, []);
      parRes.get(p.ressource).push(p);
    }
    const ressources = [...etat.rapport.ressources];
    if (parRes.has('(hors ressource)')) ressources.push({ nom: '(hors ressource)', chemin: '', fichiers: 0 });
    const poids = { critique: 0, eleve: 1, moyen: 2, info: 3 };
    ressources.sort((a, b) => {
      const pa = pireNiveau(parRes.get(a.nom) || []); const pb = pireNiveau(parRes.get(b.nom) || []);
      return (pa ? poids[pa] : 9) - (pb ? poids[pb] : 9) || a.nom.localeCompare(b.nom);
    });
    for (const r of ressources) {
      const liste = parRes.get(r.nom) || [];
      const pire = pireNiveau(liste) || 'sain';
      const decompte = liste.length ? t('probleme', liste.length) : t('rien_trouve');
      const nom = nomRessource(r.nom);
      radio.append(el('button', {
        class: `case${etat.ressource === r.nom ? ' choisie' : ''}`, 'data-pire': pire,
        title: `${nom} : ${decompte}${r.escrow ? t('escrow') : ''}`,
        'aria-label': `${nom}, ${decompte}`,
        onmouseenter: () => { $('radio-legende').textContent = `${nom} · ${decompte}`; },
        onmouseleave: () => { $('radio-legende').textContent = legendeRadio(); },
        onclick: () => {
          etat.ressource = etat.ressource === r.nom ? null : r.nom;
          construireRadio(); rendreListe();
        },
      }));
    }
    $('radio-legende').textContent = legendeRadio();
  }
  function legendeRadio() {
    return etat.ressource ? t('filtre_sur', nomRessource(etat.ressource)) : t('legende');
  }

  function filtrer(categorie = etat.categorie) {
    const q = etat.recherche.toLowerCase();
    return etat.rapport.problemes.filter((p) => {
      if (etat.ignores.has(cleIgnore(p))) return false;
      if (!etat.niveaux.has(p.niveau)) return false;
      if (categorie !== 'tout' && CATEGORIES[p.categorie] !== categorie) return false;
      if (etat.ressource && p.ressource !== etat.ressource) return false;
      if (q && !(`${p.fichier} ${p.ressource} ${tp(p, 'titre')}`.toLowerCase().includes(q))) return false;
      return true;
    });
  }

  function rendreListe() {
    const liste = $('liste');
    const visibles = filtrer();
    etat.visibles = visibles;
    for (const b of document.querySelectorAll('#onglets button')) {
      let nb = b.querySelector('.nb');
      if (!nb) { nb = el('span', { class: 'nb' }); b.append(nb); }
      nb.textContent = filtrer(b.dataset.cat).length;
    }
    liste.replaceChildren();
    if (!visibles.length) {
      const rien = !etat.rapport.problemes.length;
      liste.append(el('div', { class: 'liste-vide' },
        el('strong', { text: rien ? t('vide_rien') : t('vide_filtre') }),
        el('span', { text: rien ? t('vide_rien_d') : t('vide_filtre_d') })));
      return;
    }
    const rang = (n) => NIVEAUX.indexOf(n);
    const pireFichier = new Map();
    for (const p of visibles) pireFichier.set(p.fichier, Math.min(pireFichier.get(p.fichier) ?? 9, rang(p.niveau)));
    const tries = [...visibles].sort((a, b) => pireFichier.get(a.fichier) - pireFichier.get(b.fichier)
      || a.fichier.localeCompare(b.fichier) || (a.ligne || 0) - (b.ligne || 0));
    let fichier = null; let groupe = null;
    const frag = document.createDocumentFragment();
    for (const p of tries) {
      if (p.fichier !== fichier) {
        fichier = p.fichier;
        groupe = el('div', { class: 'groupe-fichier' }, el('h4', { title: p.fichier }, el('bdi', { text: p.fichier || nomRessource(p.ressource) })));
        frag.append(groupe);
      }
      const sous = p.categorie === 'syntaxe' ? tp(p, 'explication') : nomRessource(p.ressource);
      groupe.append(el('button', {
        class: `probleme${etat.choisi === p.id ? ' choisi' : ''}`, 'data-niveau': p.niveau, 'data-id': p.id,
        onclick: () => choisirProbleme(p.id),
      }, el('span', {}, el('span', { class: 'titre', text: tp(p, 'titre') }), el('div', { class: 'sous', text: sous })),
      el('span', { class: 'ligne-num', text: p.ligne ? `L${p.ligne}` : '' })));
    }
    liste.append(frag);
  }

  function choisirProbleme(id) {
    etat.choisi = id;
    for (const b of document.querySelectorAll('.probleme')) b.classList.toggle('choisi', Number(b.dataset.id) === id);
    const p = etat.rapport.problemes.find((x) => x.id === id);
    rendreDetail(p);
    const b = document.querySelector(`.probleme[data-id="${id}"]`);
    if (b) b.scrollIntoView({ block: 'nearest' });
  }

  function rendreDetail(p) {
    const zone = $('detail');
    zone.replaceChildren();
    if (!p) {
      zone.append(el('div', { class: 'detail-vide' }, el('p', { text: t('detail_vide') })));
      return;
    }
    const lieu = p.fichier ? `${p.fichier}${p.ligne ? t('ligne', p.ligne) : ''}` : nomRessource(p.ressource);
    const corps = el('div', { class: 'detail', 'data-niveau': p.niveau });
    corps.append(el('div', {},
      el('span', { class: 'detail-niveau', text: `${nomNiveau(p.niveau)}${p.categorie === 'syntaxe' ? ` · ${t('syntaxe')}` : ''}` }),
      el('h2', { text: tp(p, 'titre') }),
      el('p', { class: 'detail-lieu', text: lieu })));
    corps.append(el('p', { class: 'detail-texte', text: tp(p, 'explication') }));
    const brut = p.brut && p.brut !== tp(p, 'explication') ? t('message_lua', p.brut) : '';
    if (brut) corps.append(el('p', { class: 'detail-message-brut', text: brut }));
    if (p.extrait && p.extrait.length) {
      const pre = el('pre', { class: 'code' });
      for (const l of p.extrait) {
        pre.append(el('div', { class: `code-ligne${l.n === p.ligne ? ' vise' : ''}` },
          el('span', { class: 'n', text: l.n }), el('span', { text: l.t || ' ' })));
      }
      corps.append(pre);
    }
    if (p.decode) {
      corps.append(el('div', { class: 'decode' }, el('h3', { text: t('decode') }), el('pre', { text: p.decode })));
    }
    if (p.autres) corps.append(el('p', { class: 'autres', text: t('autres', p.autres) }));
    corps.append(el('div', { class: 'detail-conseil' }, el('strong', { text: t('que_faire') }), el('span', { text: tp(p, 'conseil') })));
    const actions = el('div', { class: 'detail-actions' });
    if (!integre && p.chemin) {
      actions.append(el('button', {
        class: 'bouton bouton-plein', text: t('ouvrir'),
        onclick: async () => { const r = await api().ouvrir(p.chemin, p.ligne || 1); if (r !== true) toast(r || t('ouvrir_ko')); },
      }));
    }
    if (p.chemin) {
      actions.append(el('button', {
        class: 'bouton', text: t('copier'),
        onclick: () => { navigator.clipboard.writeText(p.chemin).then(() => toast(t('copie_ok')), () => toast(t('copie_ko'))); },
      }));
    }
    actions.append(el('button', {
      class: 'bouton', text: t('ignorer'), title: t('ignorer_t'),
      onclick: () => {
        etat.ignores.add(cleIgnore(p));
        ecrireStockage('ns-ignores', [...etat.ignores]);
        const i = etat.visibles.findIndex((x) => x.id === p.id);
        construireFiltres(); construireRadio(); rendreListe();
        const suivant = etat.visibles[Math.min(i, etat.visibles.length - 1)];
        if (suivant) choisirProbleme(suivant.id); else rendreDetail(null);
        toast(t('ignore_ok'));
      },
    }));
    corps.append(actions);
    zone.append(corps);
    zone.scrollTop = 0;
  }

  $('choisir').addEventListener('click', (e) => { e.stopPropagation(); choisir(); });
  $('depot').addEventListener('click', choisir);
  $('depot').addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choisir(); } });
  for (const evt of ['dragenter', 'dragover']) {
    document.addEventListener(evt, (e) => { e.preventDefault(); $('depot').classList.add('survol'); });
  }
  for (const evt of ['dragleave', 'drop']) {
    document.addEventListener(evt, (e) => { e.preventDefault(); $('depot').classList.remove('survol'); });
  }
  $('arreter').addEventListener('click', () => { const a = api(); if (a) a.arreter(); $('analyse-titre').textContent = t('arret'); });
  $('r-nouvelle').addEventListener('click', () => { afficherRecents(); ecran('accueil'); });
  $('r-relancer').addEventListener('click', () => lancer(etat.rapport.racine));
  $('r-export-html').addEventListener('click', async () => {
    const r = await api().exporter(etat.langue);
    if (r) toast(r);
  });
  $('tout-voir').addEventListener('click', () => { etat.ressource = null; construireRadio(); rendreListe(); });
  $('recherche').addEventListener('input', (e) => { etat.recherche = e.target.value.trim(); rendreListe(); });
  for (const b of document.querySelectorAll('#onglets button')) {
    b.addEventListener('click', () => {
      etat.categorie = b.dataset.cat;
      for (const x of document.querySelectorAll('#onglets button')) x.setAttribute('aria-selected', String(x === b));
      rendreListe();
    });
  }
  document.addEventListener('keydown', (e) => {
    if (app.dataset.ecran !== 'resultats' || e.target.tagName === 'INPUT') return;
    if (e.key !== 'ArrowDown' && e.key !== 'ArrowUp') return;
    e.preventDefault();
    const ids = [...document.querySelectorAll('.probleme')].map((b) => Number(b.dataset.id));
    if (!ids.length) return;
    const i = ids.indexOf(etat.choisi);
    const j = e.key === 'ArrowDown' ? Math.min(ids.length - 1, i + 1) : Math.max(0, i - 1);
    choisirProbleme(ids[i < 0 ? 0 : j]);
  });

  const langueForcee = new URLSearchParams(location.search).get('lang');
  appliquerLangue(langueForcee === 'fr' || langueForcee === 'en' ? langueForcee
    : (integre && window.LANGUE_RAPPORT && !lireStockage('ns-langue', null)) ? window.LANGUE_RAPPORT : langueInitiale());
  if (integre) {
    document.body.classList.add('rapport');
    etat.niveaux = new Set(NIVEAUX);
    montrerResultats(integre);
  } else {
    decorDepot();
    afficherRecents();
    window.addEventListener('pywebviewready', async () => {
      const d = await api().dossier_initial();
      if (d) lancer(d);
    });
  }
})();
