# Solution avec findspark pour EMR
# findspark gère automatiquement la configuration Java et Spark

print("🔧 Configuration avec findspark...")
print("=" * 70)

# 1. Installer findspark
print("\n1️⃣  Installation de findspark...")
import subprocess
import sys

try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'findspark', '--user', '--quiet'])
    print("✅ findspark installé")
except Exception as e:
    print(f"⚠️  Erreur lors de l'installation: {e}")
    print("   (findspark peut déjà être installé)")

# 2. Utiliser findspark
print("\n2️⃣  Initialisation de findspark...")
import findspark

# Chercher Spark automatiquement
# findspark va chercher dans les chemins courants d'EMR
try:
    # Essayer d'abord sans paramètre (recherche automatique)
    findspark.init()
    print("✅ findspark initialisé (recherche automatique)")
except Exception as e:
    print(f"⚠️  Recherche automatique échouée: {e}")
    print("   Tentative avec chemin explicite...")
    
    # Essayer avec le chemin EMR standard
    spark_paths = [
        '/usr/lib/spark',
        '/opt/spark',
    ]
    
    for spark_path in spark_paths:
        try:
            findspark.init(spark_path)
            print(f"✅ findspark initialisé avec: {spark_path}")
            break
        except:
            continue
    else:
        print("❌ Impossible d'initialiser findspark")
        raise Exception("findspark.init() a échoué")

# 3. Vérifier la configuration
print("\n3️⃣  Vérification de la configuration...")
import os
print(f"JAVA_HOME: {os.environ.get('JAVA_HOME', 'Non défini')}")
print(f"SPARK_HOME: {os.environ.get('SPARK_HOME', 'Non défini')}")

# 4. Créer SparkSession
print("\n4️⃣  Création de SparkSession...")
print("-" * 70)

from pyspark.sql import SparkSession

try:
    spark = (SparkSession
             .builder
             .appName('P8')
             .config("spark.sql.parquet.writeLegacyFormat", 'true')
             .getOrCreate()
    )
    
    print("✅ SparkSession créée avec succès!")
    print(f"   Spark version: {spark.version}")
    print(f"   Spark master: {spark.sparkContext.master}")
    print(f"   App name: {spark.sparkContext.appName}")
    
except Exception as e:
    print(f"❌ Erreur lors de la création de SparkSession:")
    print(f"   {type(e).__name__}: {e}")
    print("\n💡 Solutions possibles:")
    print("   1. Redémarrer le serveur JupyterHub")
    print("   2. Vérifier que le cluster EMR est actif")
    print("   3. Utiliser le kernel PySpark (si disponible)")
    raise

print("\n" + "=" * 70)
print("✅ Configuration terminée! Spark est prêt à être utilisé.")
print("💡 Testez avec: spark.range(10).show()")
