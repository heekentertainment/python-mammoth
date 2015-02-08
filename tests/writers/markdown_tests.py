from __future__ import unicode_literals

from nose.tools import istest, assert_equal

from mammoth.writers.markdown import MarkdownWriter


@istest
def special_markdown_characters_are_escaped():
    writer = _create_writer()
    writer.text(r"\*")
    assert_equal(r"\\\*", writer.as_string())


@istest
def unrecognised_elements_are_treated_as_normal_text():
    writer = _create_writer()
    writer.start("blah");
    writer.text("Hello");
    writer.end("blah");
    assert_equal("Hello", writer.as_string())


@istest
def paragraphs_are_terminated_with_double_new_line():
    writer = _create_writer()
    writer.start("p");
    writer.text("Hello");
    writer.end("p");
    assert_equal("Hello\n\n", writer.as_string())


@istest
def h1_elements_are_converted_to_heading_with_leading_hash():
    writer = _create_writer()
    writer.start("h1");
    writer.text("Hello");
    writer.end("h1");
    assert_equal("# Hello\n\n", writer.as_string())


@istest
def h6_elements_are_converted_to_heading_with_six_leading_hashes():
    writer = _create_writer()
    writer.start("h6");
    writer.text("Hello");
    writer.end("h6");
    assert_equal("###### Hello\n\n", writer.as_string())


@istest
def br_is_written_as_two_spaces_followed_by_newline():
    writer = _create_writer()
    writer.text("Hello");
    writer.self_closing("br");
    assert_equal("Hello  \n", writer.as_string())


@istest
def strong_text_is_surrounded_by_two_underscores():
    writer = _create_writer()
    writer.text("Hello ");
    writer.start("strong");
    writer.text("World")
    writer.end("strong")
    assert_equal("Hello __World__", writer.as_string())


@istest
def emphasised_text_is_surrounded_by_one_asterix():
    writer = _create_writer()
    writer.text("Hello ");
    writer.start("em");
    writer.text("World")
    writer.end("em")
    assert_equal("Hello *World*", writer.as_string())


@istest
def anchor_tags_are_written_as_hyperlinks():
    writer = _create_writer()
    writer.start("a", {"href": "http://example.com"});
    writer.text("Hello");
    writer.end("a");
    assert_equal("[Hello](http://example.com)", writer.as_string())
    

@istest
def anchor_tags_without_href_attribute_are_treated_as_ordinary_text():
    writer = _create_writer()
    writer.start("a");
    writer.text("Hello");
    writer.end("a");
    assert_equal("Hello", writer.as_string())
    

@istest
def elements_with_ids_have_anchor_tags_with_ids_appended_to_start_of_markdown_element():
    writer = _create_writer()
    writer.start("h1", {"id": "start"})
    writer.text("Hello")
    writer.end("h1")
    assert_equal('# <a id="start"></a>Hello\n\n', writer.as_string())
    

@istest
def links_have_anchors_before_opening_square_bracket():
    writer = _create_writer()
    writer.start("a", {"href": "http://example.com", "id": "start"})
    writer.text("Hello")
    writer.end("a")
    assert_equal('<a id="start"></a>[Hello](http://example.com)', writer.as_string())


def _create_writer():
    return MarkdownWriter()