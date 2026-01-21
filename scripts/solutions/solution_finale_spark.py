# Solution finale pour Spark sur EMR avec JupyterHub
# Exécutez ce code dans une NOUVELLE cellule après avoir installé findspark

print("🔧 Configuration Spark avec findspark...")
print("=" * 70)

# 1. Installer findspark (si pas déjà fait)
import subprocess
import sys

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'findspark', '--user'], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ findspark installé")
except:
    print("ℹ️  findspark déjà installé ou installation en cours...")

# 2. Recharger sys.path pour trouver findspark
import importlib
import site
site.addsitedir(f"{os.environ.get('HOME', '/home/hadoop')}/.local/lib/python3.9/site-packages")

# 3. Importer findspark
try:
    import findspark
    print("✅ findspark importé")
except ImportError:
    # Essayer de recharger
    importlib.invalidate_caches()
    try:
        import findspark
        print("✅ findspark importé (après rechargement)")
    except ImportError:
        print("❌ findspark non trouvé")
        print("💡 Redémarrez le kernel Python et réessayez")
        raise

# 4. Initialiser findspark
print("\n🚀 Initialisation de findspark...")
try:
    # Essayer la recherche automatique
    findspark.init()
    print("✅ findspark initialisé (recherche automatique)")
except Exception as e:
    print(f"⚠️  Recherche automatique échouée: {e}")
    # Essayer avec chemin explicite
    spark_paths = ['/usr/lib/spark', '/opt/spark']
    for spark_path in spark_paths:
        try:
            findspark.init(spark_path)
            print(f"✅ findspark initialisé avec: {spark_path}")
            break
        except:
            continue
    else:
        print("❌ Impossible d'initialiser findspark")
        raise

# 5. Vérifier la configuration
import os
print(f"\n📋 Configuration:")
print(f"JAVA_HOME: {os.environ.get('JAVA_HOME', 'Non défini')}")
print(f"SPARK_HOME: {os.environ.get('SPARK_HOME', 'Non défini')}")

# 6. Créer SparkSession
print("\n🚀 Création de SparkSession...")
print("-" * 70)

from pyspark.sql import SparkSession

spark = (SparkSession
         .builder
         .appName('P8')
         .config("spark.sql.parquet.writeLegacyFormat", 'true')
         .getOrCreate()
)

print("✅ SparkSession créée avec succès!")
print(f"   Spark version: {spark.version}")
print(f"   Spark master: {spark.sparkContext.master}")

print("\n" + "=" * 70)
print("✅ Configuration terminée!")
