# Solution : Configurer Spark pour utiliser YARN sur EMR
# Sur EMR, Spark doit utiliser YARN, pas le mode local

import os
import sys

print("🔧 Configuration Spark pour EMR avec YARN...")
print("=" * 70)

# 1. Configurer les variables d'environnement pour YARN
os.environ['SPARK_HOME'] = '/usr/lib/spark'
os.environ['HADOOP_CONF_DIR'] = '/etc/hadoop/conf'
os.environ['YARN_CONF_DIR'] = '/etc/hadoop/conf'

# 2. Utiliser findspark
try:
    import findspark
    findspark.init('/usr/lib/spark')
    print("✅ findspark initialisé")
except:
    print("⚠️  findspark non disponible, continuation...")

# 3. Configurer Spark pour utiliser YARN
print("\n🚀 Création de SparkSession avec YARN...")
print("-" * 70)

from pyspark.sql import SparkSession

try:
    # Configuration pour EMR/YARN
    spark = (SparkSession
             .builder
             .appName('P8')
             .config("spark.sql.parquet.writeLegacyFormat", 'true')
             .config("spark.submit.deployMode", "client")
             .config("spark.master", "yarn")
             .getOrCreate()
    )
    
    print("✅ SparkSession créée avec succès!")
    print(f"   Spark version: {spark.version}")
    print(f"   Spark master: {spark.sparkContext.master}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    print("\n💡 Tentative sans configuration YARN explicite...")
    
    # Essayer sans configurer YARN explicitement
    spark = (SparkSession
             .builder
             .appName('P8')
             .config("spark.sql.parquet.writeLegacyFormat", 'true')
             .getOrCreate()
    )
    
    print("✅ SparkSession créée (sans YARN explicite)")
    print(f"   Spark version: {spark.version}")

print("\n" + "=" * 70)
print("✅ Configuration terminée!")
