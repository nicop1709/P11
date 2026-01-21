# 🔧 Scripts du Projet EMR

Ce répertoire contient tous les scripts shell (.sh) et Python (.py) utilisés pour configurer, gérer et dépanner le projet EMR.

## 📁 Structure des scripts

### ⚙️ Setup - Configuration initiale
Scripts pour configurer l'infrastructure AWS et EMR :

- **creer_cluster_emr.sh** - Création interactive d'un cluster EMR
- **creer_roles_emr.sh** - Création des rôles IAM nécessaires pour EMR
- **creer_tunnel_ssh.sh** - Configuration du tunnel SSH pour accéder au cluster
- **creer_cle_region.sh** - Création d'une clé EC2 dans une région spécifique
- **setup_emr_permissions.sh** - Configuration des permissions EMR

### 🔍 Verification - Vérification et diagnostic
Scripts pour vérifier l'état du système et diagnostiquer les problèmes :

- **check_emr.sh** - Vérification rapide de l'état EMR
- **diagnose_aws.sh** - Diagnostic complet de la configuration AWS
- **verifier_clusters.sh** - Vérification de l'état des clusters EMR
- **verifier_etat_complet.sh** - Vérification complète (cluster, tunnel, proxy)
- **verifier_permissions.sh** - Vérification des permissions IAM
- **verifier_tunnel_ssh.sh** - Vérification du tunnel SSH

### 🌐 Network - Gestion réseau et connexions
Scripts pour gérer les connexions réseau, tunnels SSH et proxy :

- **gerer_proxy_mac.sh** - Gestion du proxy système Mac (activation/désactivation)
- **relancer_tunnel_ssh.sh** - Relance automatique du tunnel SSH avec options de stabilité
- **redemarrer_connexion_jupyter.sh** - Redémarrage de la connexion JupyterHub

### 🛠️ Utils - Utilitaires
Scripts utilitaires et de test :

- **trouver_cle_ec2.sh** - Trouver une clé EC2 dans une région
- **trouver_groupe_securite.sh** - Trouver le groupe de sécurité EMR
- **test_emr_simple.sh** - Test simple de connexion EMR
- **test_proxy.sh** - Test de la configuration du proxy

### 🐍 Solutions - Scripts Python de solutions
Scripts Python contenant des solutions aux problèmes rencontrés :

- **solution_finale_spark.py** - Solution finale pour configurer Spark
- **solution_findspark_emr.py** - Solution utilisant findspark
- **solution_java_conda.py** - Solution pour Java dans l'environnement conda
- **solution_yarn_emr.py** - Configuration Spark avec YARN
- **diagnostic_complet_jupyterhub.py** - Diagnostic complet de l'environnement JupyterHub

### ⚙️ Config - Configuration Spark
Scripts Python pour configurer Spark sur EMR :

- **config_spark_emr_exact.py** - Configuration Spark avec chemins exacts
- **configurer_spark_emr.py** - Configuration générale de Spark pour EMR

## 🚀 Utilisation

### Scripts Shell

Tous les scripts shell sont exécutables et peuvent être lancés directement :

```bash
# Exemple : Créer un cluster EMR
./scripts/setup/creer_cluster_emr.sh

# Exemple : Vérifier l'état complet
./scripts/verification/verifier_etat_complet.sh

# Exemple : Gérer le proxy Mac
./scripts/network/gerer_proxy_mac.sh
```

### Scripts Python

Les scripts Python peuvent être exécutés directement ou importés dans un notebook :

```bash
# Exemple : Diagnostic JupyterHub
python scripts/solutions/diagnostic_complet_jupyterhub.py

# Exemple : Configuration Spark
python scripts/config/config_spark_emr_exact.py
```

## 📊 Statistiques

- **Total de scripts** : 25 fichiers
- **Scripts shell (.sh)** : 18
- **Scripts Python (.py)** : 7

### Répartition par catégorie

- **Setup** : 5 scripts
- **Verification** : 6 scripts
- **Network** : 3 scripts
- **Utils** : 4 scripts
- **Solutions** : 5 scripts
- **Config** : 2 scripts

## 🔐 Permissions

Assurez-vous que les scripts shell ont les permissions d'exécution :

```bash
chmod +x scripts/**/*.sh
```

## 📝 Notes

- Les scripts sont conçus pour fonctionner sur macOS
- Certains scripts nécessitent AWS CLI configuré
- Les scripts de setup peuvent créer des ressources AWS facturées
- Consultez la documentation dans `docs/` pour plus de détails sur chaque script

---

*Dernière mise à jour : 2026-01-21*
