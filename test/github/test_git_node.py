import pytest

from app.github.git_node import GitNode


def test_add_one_level_blob_path_to_root():
    root = GitNode.root()
    root.add_blob('foobar')
    assert len(root.children) == 1
    assert root.children[0].name == 'foobar'
    assert root.children[0].parent == root
    assert not root.children[0].is_tree


def test_add_one_level_tree_path_to_root():
    root = GitNode.root()
    root.add_tree('foobar')
    assert len(root.children) == 1
    assert root.children[0].name == 'foobar'
    assert root.children[0].parent == root
    assert root.children[0].is_tree


def test_add_one_level_path_to_root_with_children():
    root = GitNode.root()
    root.add_blob('hearts')
    root.add_blob('diamonds')
    root.add_blob('clubs')
    root.add_blob('spades')

    root.add_blob('foobar')
    assert len(root.children) == 5
    assert root.children[4].name == 'foobar'
    assert root.children[4].parent == root
    assert not root.children[4].is_tree


def test_add_one_level_path_that_already_exists_in_tree():
    root = GitNode.root()
    root.add_blob('hearts')
    root.add_blob('diamonds')
    root.add_blob('clubs')
    root.add_blob('spades')

    root.add_blob('clubs')
    assert len(root.children) == 4


def test_add_path_to_node_that_is_not_tree():
    root = GitNode('foobar', None, False)

    with pytest.raises(Exception) as e:
        root.add_blob('foo/bar/ber')

    assert str(e.value) == 'Path "foobar" is not a tree.'


def test_add_multilevel_path_to_tree():
    root = GitNode.root()
    root.add_blob('foo/bar/ber')

    assert len(root.children) == 1
    assert root.children[0].name == 'foo'
    assert root.children[0].is_tree

    assert len(root.children[0].children) == 1
    assert root.children[0].children[0].name == 'bar'
    assert root.children[0].children[0].is_tree

    assert len(root.children[0].children[0].children) == 1
    assert root.children[0].children[0].children[0].name == 'ber'
    assert not root.children[0].children[0].children[0].is_tree


def test_add_multilevel_path_to_tree_that_already_has_some_nodes():
    root = GitNode.root()
    root.add_tree('foo/bar')

    root.add_blob('foo/bar/ber')

    assert len(root.children) == 1
    assert root.children[0].name == 'foo'
    assert root.children[0].is_tree

    assert len(root.children[0].children) == 1
    assert root.children[0].children[0].name == 'bar'
    assert root.children[0].children[0].is_tree

    assert len(root.children[0].children[0].children) == 1
    assert root.children[0].children[0].children[0].name == 'ber'
    assert not root.children[0].children[0].children[0].is_tree


def test_add_multilevel_path_to_tree_that_already_has_all_nodes():
    root = GitNode.root()
    root.add_blob('foo/bar/ber')

    root.add_blob('foo/bar/ber')

    assert len(root.children) == 1
    assert root.children[0].name == 'foo'
    assert root.children[0].is_tree

    assert len(root.children[0].children) == 1
    assert root.children[0].children[0].name == 'bar'
    assert root.children[0].children[0].is_tree

    assert len(root.children[0].children[0].children) == 1
    assert root.children[0].children[0].children[0].name == 'ber'
    assert not root.children[0].children[0].children[0].is_tree


def test_add_multilevel_path_to_tree_that_already_has_some_parts_but_types_mismatch():
    root = GitNode.root()
    root.add_blob('foo/bar')

    with pytest.raises(Exception) as e:
        root.add_blob('foo/bar/ber')

    assert str(e.value) == 'Path "foo/bar" is not a tree.'


def test_one_level_blob_path_string():
    assert GitNode('foobar', None, False).path == 'foobar'


def test_one_level_tree_path_string():
    assert GitNode('foobar', None, True).path == 'foobar'


def test_multilevel_path_string():
    root = GitNode.root('/')
    root.add_blob('foo/bar/ber')
    assert (root.path) == '/'
    assert (root.children[0].path) == '/foo'
    assert (root.children[0].children[0].path) == '/foo/bar'
    assert (root.children[0].children[0].children[0].path) == '/foo/bar/ber'


def test_match_single_unix_shell_style_wildcard_pattern():
    root = GitNode.root('/init.d')
    assert root.match('/[Ii]*.d')


def test_mismatch_single_unix_shell_style_wildcard_pattern():
    root = GitNode.root('/init.d')
    assert not root.match('*.bla')


def test_match_multiple_unix_shell_style_wildcard_patterns():
    root = GitNode.root('/init.d')
    assert root.match_any(['foobar', '/i*.d', '/init.*'])


def test_mismatch_multiple_unix_shell_style_wildcard_patterns():
    root = GitNode.root('/init.d')
    assert not root.match_any(['foo', 'bar', 'foo*.d'])


def test_shallow_search_with_matches():
    root = GitNode.root()
    root.add_blob('foo.txt')
    root.add_blob('foo.txts')
    root.add_blob('foo.pdf')
    root.add_blob('foobar.txt')
    root.add_blob('foofoo.txt')
    root.add_blob('bar.pdf')

    results = root.shallow_search('*.txt')
    assert [r.path for r in results] == [
        'foo.txt',
        'foobar.txt',
        'foofoo.txt'
    ]


def test_shallow_search_without_matches():
    root = GitNode.root()
    root.add_blob('foo.txt')
    root.add_blob('foo.txts')
    root.add_blob('foo.pdf')
    root.add_blob('foobar.txt')
    root.add_blob('foofoo.txt')
    root.add_blob('bar.pdf')

    assert root.shallow_search('*.pdfs') == []


@pytest.fixture
def foobar_tree():
    root = GitNode.root()
    root.add_blob('foo/bar/readme.txt')
    root.add_blob('foo/bar/readme.md')
    root.add_blob('foo/bla/blerg/wtf')
    root.add_blob('foo/bla/readme.txt')
    root.add_blob('flu/beer/readme.txt')
    root.add_blob('flu/beer/readme.md')
    root.add_blob('flu/beer/LICENSE')
    root.add_tree('flu/beer/beer')
    root.add_blob('flu/beer/beer/script.sh')
    root.add_blob('flu/beer/document.pdf')
    root.add_tree('foo/beer/beer')
    root.add_tree('foo/beer/blur')
    root.add_blob('blur')
    return root


def test_deep_search_with_matches(foobar_tree):
    results = foobar_tree.deep_search('b*r')
    assert set([r.path for r in results]) == set([
        'foo/bar',
        'foo/beer',
        'foo/beer/beer',
        'foo/beer/blur',
        'flu/beer',
        'flu/beer/beer',
        'blur'
    ])


def test_deep_search_without_matches(foobar_tree):
    assert foobar_tree.deep_search('reports') == []


def test_search_siblings_with_matches(foobar_tree):
    node = foobar_tree.navigate('flu/beer/readme.md')
    results = node.search_siblings('*.*')
    assert set([r.path for r in results]) == set([
        'flu/beer/readme.txt',
        'flu/beer/document.pdf'
    ])


def test_search_siblings_without_matches(foobar_tree):
    node = foobar_tree.navigate('flu/beer/readme.md')
    assert node.search_siblings('*.doc') == []


def test_search_siblings_root(foobar_tree):
    assert foobar_tree.search_siblings('*') == []


def test_successfully_navigate_path(foobar_tree):
    assert foobar_tree.navigate('foo/bar/readme.md').name == 'readme.md'
    assert foobar_tree.navigate('foo/beer').name == 'beer'


def test_fail_to_navigate_path(foobar_tree):
    assert foobar_tree.navigate('foo/beer/readme.pdf') is None
    assert foobar_tree.navigate('foobar') is None
