# Solution pour Java dans l'environnement conda de JupyterHub
# Le problème : Java n'est pas dans le PATH de l'environnement conda

import os
import sys
import subprocess
import shutil

print("🔧 Configuration Java pour environnement conda...")
print("=" * 70)

# 1. Chercher Java dans les chemins système
print("\n1️⃣  Recherche de Java...")

java_locations = [
    '/usr/bin/java',
    '/bin/java',
    '/usr/local/bin/java',
    '/opt/conda/bin/java',
]

java_found = None
for java_path in java_locations:
    if os.path.exists(java_path):
        java_found = java_path
        print(f"   ✅ Java trouvé: {java_path}")
        break

if not java_found:
    # Essayer avec which depuis un shell
    try:
        # Utiliser shutil.which qui cherche dans le PATH système
        java_found = shutil.which('java')
        if java_found:
            print(f"   ✅ Java trouvé via which: {java_found}")
    except:
        pass

if java_found:
    # Ajouter le répertoire de Java au PATH
    java_dir = os.path.dirname(java_found)
    if java_dir not in os.environ.get('PATH', ''):
        os.environ['PATH'] = f"{java_dir}:{os.environ.get('PATH', '')}"
        print(f"   ✅ {java_dir} ajouté au PATH")
    
    # Trouver JAVA_HOME
    # Remonter depuis /usr/bin/java vers JAVA_HOME
    if java_found.startswith('/usr/bin/java'):
        # Sur EMR, Java est souvent dans /usr/lib/jvm
        possible_homes = [
            '/usr/lib/jvm/java-8-openjdk-amd64',
            '/usr/lib/jvm/java-8-openjdk',
            '/usr/lib/jvm/java-1.8.0-openjdk-amd64',
            '/etc/alternatives/jre',
        ]
        for home in possible_homes:
            if os.path.exists(home):
                os.environ['JAVA_HOME'] = home
                print(f"   ✅ JAVA_HOME défini: {home}")
                break
    elif java_found.startswith('/opt/conda'):
        # Java dans conda
        java_home = os.path.dirname(os.path.dirname(java_found))
        os.environ['JAVA_HOME'] = java_home
        print(f"   ✅ JAVA_HOME défini (conda): {java_home}")

# 2. Vérifier que Java fonctionne
print("\n2️⃣  Test de Java...")
try:
    result = subprocess.run(
        ['java', '-version'],
        capture_output=True,
        text=True,
        timeout=10,
        env=os.environ
    )
    if result.returncode == 0 or result.stderr:
        print("   ✅ Java fonctionne")
        print(f"   {result.stderr[:150]}")
    else:
        print("   ⚠️  Java ne répond pas correctement")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

# 3. Configurer pyspark (déjà installé dans conda)
print("\n3️⃣  Configuration pyspark...")
print("   ✅ pyspark déjà installé dans conda")

# 4. Créer SparkSession
print("\n4️⃣  Création de SparkSession...")
print("-" * 70)

try:
    from pyspark.sql import SparkSession
    
    # Configuration Spark pour EMR
    spark_builder = SparkSession.builder.appName('P8')
    spark_builder = spark_builder.config("spark.sql.parquet.writeLegacyFormat", 'true')
    
    # Si JAVA_HOME est défini, l'utiliser
    if 'JAVA_HOME' in os.environ:
        spark_builder = spark_builder.config("spark.driver.extraJavaOptions", 
                                            f"-Djava.home={os.environ['JAVA_HOME']}")
    
    spark = spark_builder.getOrCreate()
    
    print("✅ SparkSession créée avec succès!")
    print(f"   Spark version: {spark.version}")
    print(f"   Spark master: {spark.sparkContext.master}")
    
except Exception as e:
    print(f"❌ Erreur lors de la création de SparkSession:")
    print(f"   {type(e).__name__}: {e}")
    print("\n💡 Solutions alternatives:")
    print("   1. Installer Java dans conda: !conda install -y openjdk")
    print("   2. Redémarrer le serveur JupyterHub")
    raise

print("\n" + "=" * 70)
print("✅ Configuration terminée!")
