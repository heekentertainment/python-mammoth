import os

from nose.tools import istest, assert_equal
import spur
import tempman

from .testing import test_path


_local = spur.LocalShell()

@istest
def html_is_printed_to_stdout_if_output_file_is_not_set():
    docx_path = test_path("single-paragraph.docx")
    result = _local.run(["mammoth", docx_path])
    assert_equal(b"", result.stderr_output)
    assert_equal(b"<p>Walking on imported air</p>", result.output)


@istest
def html_is_written_to_file_if_output_file_is_set():
    with tempman.create_temp_dir() as temp_dir:
        output_path = os.path.join(temp_dir.path, "output.html")
        docx_path = test_path("single-paragraph.docx")
        result = _local.run(["mammoth", docx_path, output_path])
        assert_equal(b"", result.stderr_output)
        assert_equal(b"", result.output)
        with open(output_path) as output_file:
            assert_equal("<p>Walking on imported air</p>", output_file.read())


@istest
def inline_images_are_included_in_output_if_writing_to_single_file():
    docx_path = test_path("tiny-picture.docx")
    result = _local.run(["mammoth", docx_path])
    assert_equal(b"""<p><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAAXNSR0IArs4c6QAAAAlwSFlzAAAOvgAADr4B6kKxwAAAABNJREFUKFNj/M+ADzDhlWUYqdIAQSwBE8U+X40AAAAASUVORK5CYII=" /></p>""", result.output)
    