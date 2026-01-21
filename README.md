# 🍎 Classification d'Images de Fruits avec AWS EMR

Projet de traitement Big Data pour la classification d'images de fruits utilisant Apache Spark, TensorFlow et AWS EMR.

## 📋 À propos du projet

Ce projet a été développé pour **Fruits!**, une start-up AgriTech qui souhaite proposer des solutions innovantes pour la récolte des fruits. L'objectif était de créer une chaîne de traitement Big Data capable de :

- Traiter de grandes quantités d'images de fruits en mode distribué
- Extraire des features à l'aide d'un modèle de deep learning (MobileNetV2)
- Réduire la dimensionnalité des données pour optimiser le stockage et les performances
- Anticiper une montée en charge future grâce à une architecture scalable sur le cloud

Le projet démontre la mise en place d'une infrastructure Big Data complète, de la configuration de l'environnement AWS jusqu'au traitement distribué de plus de 42 000 images.

## 🏗️ Architecture technique

### Stack technologique

- **Calcul distribué** : Apache Spark 4.0.1 avec PySpark
- **Deep Learning** : TensorFlow 2.20.0 avec MobileNetV2 (transfer learning)
- **Cloud** : AWS EMR (Elastic MapReduce)
- **Stockage** : Amazon S3 (bucket `p11-nicop-data`)
- **Réduction de dimensionnalité** : PCA avec 50 composantes principales
- **Format de données** : Parquet (compression Snappy)

### Infrastructure AWS

Le projet utilise un cluster EMR configuré avec :

- **1 nœud maître + 2 nœuds workers** (type `m5.xlarge`)
- **Région** : `eu-west-3` (Paris)
- **Applications** : Spark, Hadoop, JupyterHub, TensorFlow
- **Connexion sécurisée** : Tunnel SSH SOCKS5 (port 8157) avec proxy système Mac

L'accès à JupyterHub se fait via un tunnel SSH sécurisé, permettant de travailler sur le cluster depuis une machine locale tout en bénéficiant de la puissance de calcul distribuée.

## 🚀 Fonctionnalités principales

### 1. Configuration et gestion de l'infrastructure

Le projet inclut une suite complète de scripts pour gérer l'infrastructure AWS :

**Scripts de configuration** :
- Création interactive de clusters EMR
- Configuration automatique des tunnels SSH
- Gestion du proxy système pour l'accès à JupyterHub
- Création et gestion des rôles IAM
- Gestion des clés EC2 par région

**Scripts de vérification** :
- Diagnostic complet de l'état du système (cluster, tunnel, proxy)
- Vérification de l'état des clusters EMR
- Tests de connectivité réseau

### 2. Pipeline de traitement des données

Le pipeline implémenté traite les images en plusieurs étapes :

1. **Chargement distribué** : 42 749 images JPG chargées depuis S3 en utilisant le format `binaryFile` de Spark
2. **Extraction de features** : Utilisation de MobileNetV2 pré-entraîné sur ImageNet pour extraire 1280 features par image
3. **Preprocessing** : Redimensionnement à 224x224 pixels et normalisation
4. **Réduction de dimensionnalité** : Application d'une PCA pour réduire à 50 dimensions (83% de variance expliquée)
5. **Sauvegarde** : Stockage au format Parquet sur S3 avec partitionnement optimisé

### 3. Optimisations techniques

Plusieurs optimisations ont été mises en place pour améliorer les performances :

- **Répartition intelligente** : Les données sont réparties sur 24 partitions pour maximiser le parallélisme
- **Broadcast des modèles** : Les poids du modèle MobileNetV2 sont broadcastés aux workers pour éviter les téléchargements répétés
- **Pandas UDF** : Utilisation de Scalar Iterator UDF pour optimiser le transfert de données entre Spark et Python
- **Format Parquet** : Stockage efficace avec compression Snappy

## 📊 Résultats

### Données traitées

- ✅ **42 749 images** traitées avec succès
- ✅ **1280 features** extraites par image (MobileNetV2)
- ✅ **50 dimensions** après réduction PCA
- ✅ **83% de variance** expliquée par la PCA

### Datasets générés

Les résultats sont stockés sur S3 dans deux datasets :

- **`Results/`** : Features complètes (1280 dimensions) - 24 partitions Parquet
- **`Results_PCA/`** : Features réduites (50 dimensions) - 2 partitions Parquet

Les données ont été validées en les relisant avec pandas, confirmant l'intégrité et la cohérence des résultats.

## 📁 Structure du projet

```
P11/
├── docs/                    # Documentation complète du projet
│   ├── guides-principaux/   # Guides essentiels
│   ├── guides-depannage/    # Solutions aux problèmes courants
│   ├── guides-configuration/# Configuration AWS
│   └── guides-pratiques/    # Informations pratiques
├── scripts/                 # Scripts d'automatisation
│   ├── setup/              # Configuration initiale
│   ├── verification/       # Vérification et diagnostic
│   ├── network/           # Gestion réseau/tunnel
│   ├── utils/             # Utilitaires
│   ├── solutions/         # Scripts Python de solutions
│   └── config/            # Configuration Spark
├── data/                   # Données locales (si présentes)
├── img/                    # Images de documentation
├── P11_Notebook_EMR.ipynb  # Notebook principal (exécuté)
└── P8_Notebook_Linux_EMR_PySpark_V1.0.ipynb  # Notebook de référence
```

## 🛠️ Démarrage rapide

### Prérequis

- AWS CLI configuré avec les credentials appropriés
- Accès à un compte AWS avec permissions EMR
- Machine locale (Mac recommandé pour les scripts de proxy)
- Clé SSH EC2 créée dans la région cible

### Étapes principales

1. **Créer un cluster EMR** :
   ```bash
   ./scripts/setup/creer_cluster_emr.sh
   ```

2. **Configurer le tunnel SSH** :
   ```bash
   ./scripts/setup/creer_tunnel_ssh.sh
   ```

3. **Activer le proxy système** :
   ```bash
   ./scripts/network/gerer_proxy_mac.sh
   ```

4. **Accéder à JupyterHub** :
   - Ouvrir `https://<master-dns>:9443` dans votre navigateur
   - Le proxy système redirige automatiquement le trafic

5. **Exécuter le notebook** :
   - Ouvrir `P11_Notebook_EMR.ipynb` dans JupyterHub
   - Suivre les cellules dans l'ordre

Pour plus de détails, consultez la [documentation complète](docs/README.md).

## 📚 Documentation

Le projet inclut une documentation complète organisée par catégories :

- **[Guides principaux](docs/guides-principaux/)** : Documentation essentielle pour comprendre et utiliser le projet
- **[Guides de dépannage](docs/guides-depannage/)** : Solutions aux problèmes courants
- **[Guides de configuration](docs/guides-configuration/)** : Configuration détaillée de l'infrastructure AWS
- **[Guides pratiques](docs/guides-pratiques/)** : Informations sur les coûts, gestion du compte AWS, etc.

## 🔒 Sécurité

Tous les scripts ont été vérifiés pour éviter l'exposition d'informations sensibles :

- ✅ Aucune clé API hardcodée
- ✅ Aucun mot de passe en clair
- ✅ Les identifiants de cluster sont demandés à l'utilisateur ou via variables d'environnement
- ✅ Les chemins de clés SSH utilisent des variables avec expansion

Consultez le [rapport de confidentialité](scripts/RAPPORT_CONFIDENTIALITE.md) pour plus de détails.

## 💰 Coûts

⚠️ **Important** : AWS EMR n'est pas gratuit, même avec le Free Tier.

- Coût estimé : ~0.50-0.60 €/heure pour un cluster m5.xlarge (1 maître + 2 workers)
- **N'oubliez pas de résilier le cluster** après utilisation pour éviter les coûts inutiles

Pour plus d'informations sur les coûts, voir [COUTS_EMR.md](docs/guides-pratiques/COUTS_EMR.md).

## 🎯 Prochaines étapes

Ce projet démontre la capacité à :

- ✅ Déployer une infrastructure Big Data sur AWS
- ✅ Traiter de grandes quantités d'images avec Spark et TensorFlow
- ✅ Optimiser les performances avec le calcul distribué
- ✅ Gérer l'infrastructure cloud de manière sécurisée

Les données traitées peuvent maintenant être utilisées pour :
- Entraîner des modèles de classification
- Créer des applications de reconnaissance de fruits
- Analyser la biodiversité des fruits

## 📝 Notes techniques

### Résolution de problèmes

Plusieurs défis techniques ont été résolus au cours du projet :

- **Configuration Spark sur EMR** : Installation de Java 17 et configuration des variables d'environnement
- **Intégration S3** : Configuration de Hadoop AWS (S3A) pour l'accès aux données
- **Connexion JupyterHub** : Mise en place d'un tunnel SSH SOCKS5 avec proxy système
- **Optimisation TensorFlow + Spark** : Utilisation de Pandas UDF et broadcast des modèles

Toutes les solutions sont documentées dans les guides de dépannage.

## 👤 Auteur

Projet réalisé dans le cadre de la formation OpenClassRooms Ingénieur IA.

## 📄 Licence

Ce projet est fourni à titre éducatif et de démonstration.

---

*Dernière mise à jour : Janvier 2026*
