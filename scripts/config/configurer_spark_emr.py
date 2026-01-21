# Configuration Spark pour EMR dans JupyterHub
# À exécuter dans la première cellule d'un notebook Python

import os
import sys
import subprocess

print("🔧 Configuration de l'environnement Spark pour EMR...")
print("=" * 50)

# 1. Configurer JAVA_HOME (Java 8 sur EMR)
java_paths = [
    '/usr/lib/jvm/java-8-openjdk-amd64',
    '/usr/lib/jvm/java-8-openjdk',
    '/usr/lib/jvm/java-1.8.0-openjdk-amd64',
    '/usr/lib/jvm/java-1.8.0-openjdk',
]

java_home_set = False
for path in java_paths:
    if os.path.exists(path):
        os.environ['JAVA_HOME'] = path
        print(f"✅ JAVA_HOME défini : {path}")
        java_home_set = True
        break

if not java_home_set:
    # Essayer de trouver Java via which
    try:
        java_path = subprocess.check_output(['which', 'java'], stderr=subprocess.STDOUT).decode().strip()
        # Extraire JAVA_HOME depuis le chemin java
        java_home = os.path.dirname(os.path.dirname(java_path))
        if os.path.exists(java_home):
            os.environ['JAVA_HOME'] = java_home
            print(f"✅ JAVA_HOME défini (via which java) : {java_home}")
            java_home_set = True
    except:
        pass

if not java_home_set:
    print("⚠️  JAVA_HOME non trouvé automatiquement")

# 2. Configurer SPARK_HOME (Spark sur EMR)
spark_paths = [
    '/usr/lib/spark',
    '/opt/spark',
]

spark_home_set = False
for path in spark_paths:
    if os.path.exists(path):
        os.environ['SPARK_HOME'] = path
        print(f"✅ SPARK_HOME défini : {path}")
        spark_home_set = True
        
        # Ajouter Spark Python au PYTHONPATH
        spark_python = f"{path}/python"
        if os.path.exists(spark_python):
            if spark_python not in sys.path:
                sys.path.insert(0, spark_python)
            print(f"✅ Spark Python ajouté au PYTHONPATH")
        
        # Ajouter py4j
        py4j_paths = [
            f"{path}/python/lib/py4j-*.zip",
            f"{path}/python/lib/py4j-*.jar",
        ]
        import glob
        for pattern in py4j_paths:
            matches = glob.glob(pattern)
            if matches:
                for match in matches:
                    if match not in sys.path:
                        sys.path.insert(0, match)
                print(f"✅ py4j trouvé et ajouté")
                break
        break

if not spark_home_set:
    print("⚠️  SPARK_HOME non trouvé")

# 3. Ajouter Spark au PATH
if 'SPARK_HOME' in os.environ:
    spark_bin = f"{os.environ['SPARK_HOME']}/bin"
    if spark_bin not in os.environ.get('PATH', ''):
        os.environ['PATH'] = f"{spark_bin}:{os.environ.get('PATH', '')}"

# 4. Vérifications
print("\n📋 Vérifications :")
print("-" * 50)

# Vérifier Java
try:
    java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT, timeout=5).decode()
    print("✅ Java disponible")
except Exception as e:
    print(f"❌ Java non disponible : {e}")

# Vérifier les variables
print(f"JAVA_HOME: {os.environ.get('JAVA_HOME', 'Non défini')}")
print(f"SPARK_HOME: {os.environ.get('SPARK_HOME', 'Non défini')}")

# Vérifier si pyspark est accessible
try:
    import pyspark
    print(f"✅ pyspark importable (version: {pyspark.__version__ if hasattr(pyspark, '__version__') else 'inconnue'})")
except ImportError as e:
    print(f"⚠️  pyspark non importable : {e}")

print("\n" + "=" * 50)
print("✅ Configuration terminée !")
print("💡 Vous pouvez maintenant créer la SparkSession dans la cellule suivante")
