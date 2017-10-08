import pytest
from textwrap import dedent


from app.platforms.jvm.maven_pom import MavenPom
from app.platforms.jvm.package_name import JvmPackageName
from app.dependency import Dependency


def test_parse_full_xml():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <modelVersion>4.0.0</modelVersion>
            <groupId>org.spire-math</groupId>
            <artifactId>kind-projector_2.10</artifactId>
            <packaging>jar</packaging>
            <description>kind-projector</description>
            <url>http://github.com/non/kind-projector</url>
            <version>0.9.4</version>
            <licenses>
                <license>
                    <name>MIT</name>
                    <url>http://opensource.org/licenses/MIT</url>
                    <distribution>repo</distribution>
                </license>
                <license>
                    <name>GPLv3</name>
                    <url>http://opensource.org/licenses/GPLv3</url>
                    <distribution>repo</distribution>
                </license>
            </licenses>
            <name>kind-projector</name>
            <organization>
                <name>org.spire-math</name>
                <url>http://github.com/non/kind-projector</url>
            </organization>
            <scm>
                <url>git@github.com:non/kind-projector.git</url>
                <connection>scm:git:git@github.com:non/kind-projector.git</connection>
            </scm>
            <developers>
                <developer>
                    <id>d_m</id>
                    <name>Erik Osheim</name>
                    <url>http://github.com/non/</url>
                </developer>
            </developers>
            <dependencies>
                <dependency>
                    <groupId>org.scala-lang</groupId>
                    <artifactId>scala-compiler</artifactId>
                    <version>2.10.6</version>
                </dependency>
                <dependency>
                    <groupId>org.scala-lang</groupId>
                    <artifactId>scala-library</artifactId>
                    <version>2.10.6</version>
                </dependency>
                <dependency>
                    <groupId>org.scalamacros</groupId>
                    <artifactId>quasiquotes_2.10</artifactId>
                    <version>2.1.0</version>
                </dependency>
                <dependency>
                    <groupId>com.novocode</groupId>
                    <artifactId>junit-interface</artifactId>
                    <version>0.11</version>
                    <scope>test</scope>
                </dependency>
                <dependency>
                    <groupId>org.ensime</groupId>
                    <artifactId>pcplod_2.10</artifactId>
                    <version>1.2.1</version>
                    <scope> test  </scope>
                </dependency>
            </dependencies>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'
    assert set(pom.runtime_dependencies) == set([
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-compiler')),
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-library')),
        Dependency.runtime(JvmPackageName('org.scalamacros', 'quasiquotes_2.10'))
    ])
    assert set(pom.development_dependencies) == set([
        Dependency.development(JvmPackageName('com.novocode', 'junit-interface')),
        Dependency.development(JvmPackageName('org.ensime', 'pcplod_2.10'))
    ])
    assert set(pom.licenses) == set(['MIT', 'GPLv3'])
    assert pom.urls == set([
        'http://github.com/non/kind-projector',
        'git@github.com:non/kind-projector.git'
    ])


def test_parse_xml_with_only_one_license():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <licenses>
                <license>
                    <name>MIT</name>
                    <url>http://opensource.org/licenses/MIT</url>
                    <distribution>repo</distribution>
                </license>
            </licenses>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.licenses == ['MIT']


def test_parse_xml_without_licenses_block():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.licenses == []


def test_parse_xml_with_empty_licenses_block():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <licenses>
            </licenses>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.licenses == []


def test_parse_xml_with_only_one_dependency():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <dependencies>
                <dependency>
                    <groupId>org.scala-lang</groupId>
                    <artifactId>scala-compiler</artifactId>
                    <version>2.10.6</version>
                </dependency>
            </dependencies>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.runtime_dependencies == [
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-compiler'))
    ]
    assert pom.development_dependencies == []


def test_parse_xml_without_dependencies_block():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.runtime_dependencies == []
    assert pom.development_dependencies == []


def test_parse_xml_with_empty_dependencies_block():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <dependencies>
            </dependencies>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.runtime_dependencies == []
    assert pom.development_dependencies == []


def test_parse_xml_without_url_tag():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.urls == set()


def test_parse_xml_with_empty_url_tag():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <url></url>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.urls == set()


def test_parse_xml_without_scm_block():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.urls == set()


def test_parse_xml_with_empty_scm_block():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <scm></scm>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.urls == set()


def test_parse_xml_with_scm_block_without_url():
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <scm>
                <connection>scm:git:git@github.com:non/kind-projector.git</connection>
            </scm>
        </project>
    ''')

    pom = MavenPom.parse(xml)
    assert pom.urls == set()


def test_parse_xml_with_whitespace_at_beginning():
    xml = '''
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.spire-math</groupId>
            <artifactId>kind-projector_2.10</artifactId>
        </project>
    '''

    pom = MavenPom.parse(xml)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'


def test_parse_xml_with_invalid_bytes_at_beginning():
    xml = '''ï»¿<?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.spire-math</groupId>
            <artifactId>kind-projector_2.10</artifactId>
        </project>
    '''

    pom = MavenPom.parse(xml)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'
