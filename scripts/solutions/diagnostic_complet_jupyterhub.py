# Diagnostic complet de l'environnement dans JupyterHub
# Exécutez ce code pour voir ce qui est disponible

import os
import sys
import subprocess
import glob

print("=" * 70)
print("🔍 DIAGNOSTIC COMPLET DE L'ENVIRONNEMENT JUPYTERHUB")
print("=" * 70)

# 1. Vérifier Python
print("\n1️⃣  Python:")
print(f"   Version: {sys.version}")
print(f"   Exécutable: {sys.executable}")

# 2. Vérifier Java
print("\n2️⃣  Java:")
try:
    result = subprocess.run(['which', 'java'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        java_path = result.stdout.strip()
        print(f"   ✅ Java trouvé: {java_path}")
        try:
            java_version = subprocess.run(['java', '-version'], capture_output=True, text=True, stderr=subprocess.STDOUT, timeout=5)
            print(f"   Version: {java_version.stdout[:100]}")
        except:
            print("   ⚠️  Impossible d'exécuter java -version")
    else:
        print("   ❌ Java non trouvé dans PATH")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 3. Vérifier JAVA_HOME
print("\n3️⃣  JAVA_HOME:")
java_home = os.environ.get('JAVA_HOME', 'Non défini')
print(f"   Actuel: {java_home}")

# Chercher Java
java_paths_to_check = [
    '/etc/alternatives/jre',
    '/usr/lib/jvm/java-8-openjdk-amd64',
    '/usr/lib/jvm/java-8-openjdk',
    '/usr/lib/jvm/java-1.8.0-openjdk-amd64',
    '/usr/lib/jvm/java-1.8.0-openjdk',
    '/usr/java',
    '/opt/java',
]

print("   Chemins vérifiés:")
for path in java_paths_to_check:
    exists = os.path.exists(path)
    java_bin = os.path.join(path, 'bin', 'java') if exists else None
    java_bin_exists = os.path.exists(java_bin) if java_bin else False
    status = "✅" if java_bin_exists else ("⚠️  (existe mais pas de bin/java)" if exists else "❌")
    print(f"   {status} {path}")

# 4. Vérifier SPARK_HOME
print("\n4️⃣  SPARK_HOME:")
spark_home = os.environ.get('SPARK_HOME', 'Non défini')
print(f"   Actuel: {spark_home}")

spark_paths_to_check = [
    '/usr/lib/spark',
    '/opt/spark',
]

print("   Chemins vérifiés:")
for path in spark_paths_to_check:
    exists = os.path.exists(path)
    spark_python = os.path.join(path, 'python') if exists else None
    spark_python_exists = os.path.exists(spark_python) if spark_python else False
    status = "✅" if spark_python_exists else ("⚠️  (existe mais pas de python/)" if exists else "❌")
    print(f"   {status} {path}")

# 5. Vérifier py4j et pyspark
print("\n5️⃣  Fichiers Spark Python:")
if os.path.exists('/usr/lib/spark/python/lib'):
    lib_dir = '/usr/lib/spark/python/lib'
    files = os.listdir(lib_dir)
    print(f"   Contenu de {lib_dir}:")
    for f in files:
        full_path = os.path.join(lib_dir, f)
        size = os.path.getsize(full_path) if os.path.isfile(full_path) else 0
        print(f"   - {f} ({size} bytes)")

# 6. Vérifier PYTHONPATH
print("\n6️⃣  PYTHONPATH:")
print(f"   Longueur: {len(sys.path)} chemins")
print("   Premiers chemins:")
for i, path in enumerate(sys.path[:10]):
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"   {status} {path}")

# 7. Vérifier si pyspark est importable
print("\n7️⃣  Import pyspark:")
try:
    import pyspark
    print(f"   ✅ pyspark importable")
    if hasattr(pyspark, '__version__'):
        print(f"   Version: {pyspark.__version__}")
    if hasattr(pyspark, '__file__'):
        print(f"   Fichier: {pyspark.__file__}")
except ImportError as e:
    print(f"   ❌ pyspark non importable: {e}")
except Exception as e:
    print(f"   ⚠️  Erreur lors de l'import: {e}")

# 8. Vérifier les variables d'environnement importantes
print("\n8️⃣  Variables d'environnement:")
env_vars = ['JAVA_HOME', 'SPARK_HOME', 'PYSPARK_PYTHON', 'PYSPARK_DRIVER_PYTHON', 'PATH']
for var in env_vars:
    value = os.environ.get(var, 'Non défini')
    if var == 'PATH':
        print(f"   {var}: {value[:200]}...")
    else:
        print(f"   {var}: {value}")

print("\n" + "=" * 70)
print("✅ Diagnostic terminé")
print("=" * 70)
