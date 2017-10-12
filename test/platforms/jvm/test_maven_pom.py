import pytest
from textwrap import dedent


from test import *
from app.platforms.jvm.maven_pom import MavenPom
from app.platforms.jvm.maven_dependency import MavenDependency
from app.platforms.jvm.package_name import JvmPackageName
from app.platforms.jvm.maven2_package_registry import Maven2PackageRegistry
from app.dependency import DependencyKind


@pytest.fixture
def registry():
    return Maven2PackageRegistry(http_compression=False)


def test_parse_scalar_xml(registry):
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
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'
    assert pom.version == '0.9.4'
    assert pom.parent is None
    assert pom.properties == {}
    assert pom.dependencies == []
    assert set(pom.licenses) == set(['MIT', 'GPLv3'])
    assert pom.urls == set([
        'http://github.com/non/kind-projector',
        'git@github.com:non/kind-projector.git'
    ])


def test_parse_xml_with_dependencies(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.spire-math</groupId>
            <artifactId>kind-projector_2.10</artifactId>
            <version>0.9.4</version>
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
                    <scope>test</scope>
                </dependency>
            </dependencies>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert set(pom.filter_dependencies(DependencyKind.RUNTIME)) == set([
        MavenDependency('org.scala-lang', 'scala-compiler'),
        MavenDependency('org.scala-lang', 'scala-library'),
        MavenDependency('org.scalamacros', 'quasiquotes_2.10')
    ])
    assert set(pom.filter_dependencies(DependencyKind.DEVELOPMENT)) == set([
        MavenDependency('com.novocode', 'junit-interface', 'test'),
        MavenDependency('org.ensime', 'pcplod_2.10', 'test')
    ])


def test_parse_xml_with_only_one_dependency(registry):
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

    pom = MavenPom.parse(xml, registry)
    assert pom.dependencies == [
        MavenDependency('org.scala-lang', 'scala-compiler')
    ]


def test_parse_xml_with_empty_dependencies_block(registry):
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

    pom = MavenPom.parse(xml, registry)
    assert pom.dependencies == []


@VCR.use_cassette('maven_pom_parse_xml_with_parent.yaml')
def test_parse_xml_with_parent(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.apache.ws.commons.axiom</groupId>
            <artifactId>axiom-parent</artifactId>
            <version>1.2.9</version>
            <parent>
                <groupId>org.apache</groupId>
                <artifactId>apache</artifactId>
                <version>7</version>
            </parent>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.parent.group_id == 'org.apache'
    assert pom.parent.artifact_id == 'apache'
    assert pom.parent.version == '7'
    assert pom.parent.parent is None


@VCR.use_cassette('maven_pom_parse_xml_with_parent_and_grandparent.yaml')
def test_parse_xml_with_parent_and_grandparent(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.apache.cxf</groupId>
            <artifactId>apache-cxf</artifactId>
            <version>2.2.5</version>
            <parent>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-parent</artifactId>
                <version>2.2.5</version>
                <relativePath>../parent</relativePath>
            </parent>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.parent.group_id == 'org.apache.cxf'
    assert pom.parent.artifact_id == 'cxf-parent'
    assert pom.parent.version == '2.2.5'
    assert pom.parent.parent.group_id == 'org.apache.cxf'
    assert pom.parent.parent.artifact_id == 'cxf'
    assert pom.parent.parent.version == '2.2.5'
    assert pom.parent.parent.parent is None


@VCR.use_cassette('maven_pom_parse_xml_with_group_id_from_parent.yaml')
def test_parse_xml_with_group_id_from_parent(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <parent>
                <groupId>org.apache.cxf</groupId>
                <artifactId>cxf-parent</artifactId>
                <version>2.2.5</version>
                <relativePath>../parent</relativePath>
            </parent>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.group_id == 'org.apache.cxf'


def test_parse_xml_with_properties(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <properties>
                <stax.impl.groupid>org.codehaus.woodstox</stax.impl.groupid>
                <stax.impl.artifact>wstx-asl</stax.impl.artifact>
                <stax.impl.version>3.2.9</stax.impl.version>
                <failIfNoTests>false</failIfNoTests>
            </properties>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.properties == {
        'stax.impl.groupid': 'org.codehaus.woodstox',
        'stax.impl.artifact': 'wstx-asl',
        'stax.impl.version': '3.2.9',
        'failIfNoTests': 'false'
    }


@VCR.use_cassette('maven_pom_parse_xml_with_properties_merged_with_parent_properties.yaml')
def test_parse_xml_with_properties_merged_with_parent_properties(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <parent>
                <groupId>org.apache</groupId>
                <artifactId>apache</artifactId>
                <version>7</version>
            </parent>
            <properties>
                <stax.impl.groupid>org.codehaus.woodstox</stax.impl.groupid>
                <stax.impl.artifact>wstx-asl</stax.impl.artifact>
                <stax.impl.version>3.2.9</stax.impl.version>
                <failIfNoTests>false</failIfNoTests>
            </properties>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.properties == {
        'stax.impl.groupid': 'org.codehaus.woodstox',
        'stax.impl.artifact': 'wstx-asl',
        'stax.impl.version': '3.2.9',
        'failIfNoTests': 'false',
        'distMgmtSnapshotsName': 'Apache Development Snapshot Repository',
        'distMgmtSnapshotsUrl': 'https://repository.apache.org/content/repositories/snapshots',
        'organization.logo': 'http://www.apache.org/images/asf_logo_wide.gif',
        'project.build.sourceEncoding': 'UTF-8',
        'sourceReleaseAssemblyDescriptor': 'source-release'
    }


def test_parse_xml_with_only_one_property(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <properties>
                <stax.impl.groupid>org.codehaus.woodstox</stax.impl.groupid>
            </properties>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.properties == {'stax.impl.groupid': 'org.codehaus.woodstox'}


def test_parse_xml_with_empty_properties_block(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <properties>
            </properties>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.properties == {}


def test_parse_xml_with_only_one_license(registry):
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

    pom = MavenPom.parse(xml, registry)
    assert pom.licenses == ['MIT']


def test_parse_xml_without_licenses_block(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.licenses == []


def test_parse_xml_with_empty_licenses_block(registry):
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

    pom = MavenPom.parse(xml, registry)
    assert pom.licenses == []


def test_parse_xml_with_scalar_license_block(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <licenses>
                <license>MIT</license>
            </licenses>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.licenses == ['MIT']


def test_parse_xml_with_empty_license_block(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <licenses>
                <license></license>
            </licenses>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.licenses == []


def test_parse_xml_without_url_tag(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.urls == set()


def test_parse_xml_with_empty_url_tag(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <url></url>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.urls == set()


def test_parse_xml_without_scm_block(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.urls == set()


def test_parse_xml_with_empty_scm_block(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <scm></scm>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.urls == set()


def test_parse_xml_with_scm_block_without_url(registry):
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

    pom = MavenPom.parse(xml, registry)
    assert pom.urls == set()


def test_parse_xml_with_whitespace_at_beginning(registry):
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

    pom = MavenPom.parse(xml, registry)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'


def test_parse_xml_with_invalid_bytes_at_beginning(registry):
    xml = '''ï»¿<?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.spire-math</groupId>
            <artifactId>kind-projector_2.10</artifactId>
        </project>
    '''

    pom = MavenPom.parse(xml, registry)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'


def test_parse_xml_ignoring_ampersand_character(registry):
    xml = dedent('''\
        <?xml version='1.0' encoding='UTF-8'?>
        <project
            xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns="http://maven.apache.org/POM/4.0.0">
            <groupId>org.spire-math</groupId>
            <artifactId>kind-projector_2.10</artifactId>
            <developers>
                <developer>
                    <id>&nbsp;</id>
                    <name>Simeon Fitch</name>
                    <url>http://www.mseedsoft.com/</url>
                    <roles>
                        <role>Developer</role>
                    </roles>
                </developer>
          </developers>
        </project>
    ''')

    pom = MavenPom.parse(xml, registry)
    assert pom.group_id == 'org.spire-math'
    assert pom.artifact_id == 'kind-projector_2.10'


@pytest.fixture
def pom(parent_pom):
    return MavenPom(
        group_id='com.example.foobar',
        artifact_id='foobar',
        version='1.2.3',
        parent=parent_pom,
        properties={
            'foo.bar': 'FooBar',
            'hello': 'hello-world'
        }
    )


@pytest.fixture
def parent_pom():
    return MavenPom(
        group_id='com.example',
        artifact_id='foobar-parent',
        version='4.5.6',
        parent=None,
        properties={
            'hiThere': 'hi_there',
            'omg': 'oh-my-god'
        }
    )


def test_get_project_builtin_properties(pom):
    assert pom.get_property('project.groupId') == 'com.example.foobar'
    assert pom.get_property('pom.groupId') == 'com.example.foobar'
    assert pom.get_property('project.artifactId') == 'foobar'
    assert pom.get_property('pom.artifactId') == 'foobar'
    assert pom.get_property('project.version') == '1.2.3'
    assert pom.get_property('pom.version') == '1.2.3'


def test_get_project_parent_builtin_properties(pom):
    assert pom.get_property('project.parent.groupId') == 'com.example'
    assert pom.get_property('pom.parent.groupId') == 'com.example'
    assert pom.get_property('project.parent.artifactId') == 'foobar-parent'
    assert pom.get_property('pom.parent.artifactId') == 'foobar-parent'
    assert pom.get_property('project.parent.version') == '4.5.6'
    assert pom.get_property('pom.parent.version') == '4.5.6'


def test_existing_property(pom):
    assert pom.get_property('foo.bar') == 'FooBar'
    assert pom.get_property('hello') == 'hello-world'


def test_existing_parent_property(pom):
    assert pom.get_property('hiThere') == 'hi_there'
    assert pom.get_property('omg') == 'oh-my-god'


def test_nonexistent_property(pom):
    assert pom.get_property('wtf') is None
    assert pom.get_property('project.wtf') is None
    assert pom.get_property('pom.wtf') is None
    assert pom.get_property('project.parent.wtf') is None
    assert pom.get_property('pom.parent.wtf') is None
