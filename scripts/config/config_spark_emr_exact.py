# Configuration Spark pour EMR - Chemins exacts
# À exécuter dans la première cellule d'un notebook Python

import os
import sys
import glob

print("🔧 Configuration de l'environnement Spark pour EMR...")
print("=" * 60)

# 1. Configurer JAVA_HOME (chemin exact trouvé sur le cluster)
java_home = '/etc/alternatives/jre'
if os.path.exists(java_home):
    os.environ['JAVA_HOME'] = java_home
    print(f"✅ JAVA_HOME: {java_home}")
else:
    # Fallback vers les chemins courants
    java_paths = [
        '/usr/lib/jvm/java-8-openjdk-amd64',
        '/usr/lib/jvm/java-8-openjdk',
        '/usr/lib/jvm/java-1.8.0-openjdk-amd64',
    ]
    for path in java_paths:
        if os.path.exists(path):
            os.environ['JAVA_HOME'] = path
            print(f"✅ JAVA_HOME (fallback): {path}")
            break

# 2. Configurer SPARK_HOME
spark_home = '/usr/lib/spark'
if os.path.exists(spark_home):
    os.environ['SPARK_HOME'] = spark_home
    print(f"✅ SPARK_HOME: {spark_home}")
    
    # Ajouter Spark Python au PYTHONPATH
    spark_python = f'{spark_home}/python'
    if os.path.exists(spark_python):
        if spark_python not in sys.path:
            sys.path.insert(0, spark_python)
        print(f"✅ Spark Python ajouté au PYTHONPATH")
    
    # Ajouter py4j (chemin exact: py4j-0.10.9.7-src.zip)
    py4j_path = f'{spark_home}/python/lib/py4j-0.10.9.7-src.zip'
    if os.path.exists(py4j_path):
        if py4j_path not in sys.path:
            sys.path.insert(0, py4j_path)
        print(f"✅ py4j ajouté: py4j-0.10.9.7-src.zip")
    else:
        # Fallback: chercher n'importe quel py4j
        py4j_pattern = f'{spark_home}/python/lib/py4j-*.zip'
        py4j_matches = glob.glob(py4j_pattern)
        if py4j_matches:
            for match in py4j_matches:
                if match not in sys.path:
                    sys.path.insert(0, match)
            print(f"✅ py4j ajouté (fallback): {py4j_matches[0]}")
        else:
            print("⚠️  py4j non trouvé")
    
    # Ajouter pyspark.zip
    pyspark_zip = f'{spark_home}/python/lib/pyspark.zip'
    if os.path.exists(pyspark_zip):
        if pyspark_zip not in sys.path:
            sys.path.insert(0, pyspark_zip)
        print(f"✅ pyspark.zip ajouté")
else:
    print("❌ SPARK_HOME non trouvé")

# 3. Vérifications finales
print("\n📋 Configuration finale:")
print("-" * 60)
print(f"JAVA_HOME: {os.environ.get('JAVA_HOME', 'Non défini')}")
print(f"SPARK_HOME: {os.environ.get('SPARK_HOME', 'Non défini')}")

# 4. Créer SparkSession
print("\n🚀 Création de la SparkSession...")
print("-" * 60)

try:
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
    print(f"   App name: {spark.sparkContext.appName}")
    
except Exception as e:
    print(f"❌ Erreur lors de la création de SparkSession:")
    print(f"   {type(e).__name__}: {e}")
    print("\n💡 Solutions possibles:")
    print("   1. Redémarrer le serveur JupyterHub")
    print("   2. Vérifier que le cluster EMR est actif")
    print("   3. Vérifier les logs du serveur")
    raise

print("\n" + "=" * 60)
print("✅ Configuration terminée! Vous pouvez maintenant utiliser Spark.")
print("💡 Testez avec: spark.range(10).show()")
