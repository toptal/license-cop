from textwrap import dedent

from app.platforms.jvm.maven_metadata import MavenMetadata


def test_parse_valid_xml_with_latest_tag():
    xml = dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <metadata>
          <groupId>org.spire-math</groupId>
          <artifactId>kind-projector_2.10</artifactId>
          <versioning>
            <latest>0.9.4</latest>
            <release>0.9.4</release>
            <versions>
              <version>0.6.3</version>
              <version>0.7.0</version>
              <version>0.7.1</version>
              <version>0.8.0</version>
              <version>0.8.1</version>
              <version>0.8.2</version>
              <version>0.9.0</version>
              <version>0.9.2</version>
              <version>0.9.3</version>
              <version>0.9.4</version>
            </versions>
            <lastUpdated>20170530144248</lastUpdated>
          </versioning>
        </metadata>
    ''')
    metadata = MavenMetadata.parse(xml)
    assert metadata.latest_version == '0.9.4'


def test_parse_valid_xml_witht_empth_latest_tag():
    xml = dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <metadata>
          <groupId>org.spire-math</groupId>
          <artifactId>kind-projector_2.10</artifactId>
          <versioning>
            <latest></latest>
            <versions>
              <version>0.6.3</version>
              <version>0.7.0</version>
              <version>0.7.1</version>
              <version>0.8.0</version>
              <version>0.8.1</version>
              <version>0.8.2</version>
              <version>0.9.0</version>
              <version>0.9.2</version>
              <version>0.9.3</version>
              <version>0.9.4</version>
            </versions>
            <lastUpdated>20170530144248</lastUpdated>
          </versioning>
        </metadata>
    ''')
    metadata = MavenMetadata.parse(xml)
    assert metadata.latest_version == '0.9.4'


def test_parse_valid_xml_without_latest_tag_and_sorted_versions():
    xml = dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <metadata>
          <groupId>org.spire-math</groupId>
          <artifactId>kind-projector_2.10</artifactId>
          <versioning>
            <versions>
              <version>0.6.3</version>
              <version>0.7.0</version>
              <version>0.7.1</version>
              <version>0.8.0</version>
              <version>0.8.1</version>
              <version>0.8.2</version>
              <version>0.9.0</version>
              <version>0.9.2</version>
              <version>0.9.3</version>
              <version>0.9.4</version>
            </versions>
            <lastUpdated>20170530144248</lastUpdated>
          </versioning>
        </metadata>
    ''')
    metadata = MavenMetadata.parse(xml)
    assert metadata.latest_version == '0.9.4'


def test_parse_valid_xml_without_latest_tag_and_not_sorted_versions():
    xml = dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <metadata>
          <groupId>org.spire-math</groupId>
          <artifactId>kind-projector_2.10</artifactId>
          <versioning>
            <versions>
              <version>0.9.3</version>
              <version>0.6.3</version>
              <version>0.7.0</version>
              <version>0.8.1</version>
              <version>0.7.1</version>
              <version>0.8.0</version>
              <version>0.9.4</version>
              <version>0.9.0</version>
              <version>0.9.2</version>
              <version>0.8.2</version>
            </versions>
            <lastUpdated>20170530144248</lastUpdated>
          </versioning>
        </metadata>
    ''')
    metadata = MavenMetadata.parse(xml)
    assert metadata.latest_version == '0.9.4'


def test_parse_valid_xml_without_latest_tag_and_only_one_version():
    xml = dedent('''\
        <?xml version="1.0" encoding="UTF-8"?>
        <metadata>
          <groupId>org.spire-math</groupId>
          <artifactId>kind-projector_2.10</artifactId>
          <versioning>
            <versions>
              <version>0.9.4</version>
            </versions>
            <lastUpdated>20170530144248</lastUpdated>
          </versioning>
        </metadata>
    ''')
    metadata = MavenMetadata.parse(xml)
    assert metadata.latest_version == '0.9.4'
