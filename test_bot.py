from bot import es_saludo, INFO


def test_saludos():
    assert es_saludo("hola")
    assert es_saludo("hola, qué tal")
    assert es_saludo("buenos días!")


def test_temas_no_son_saludo():
    assert not es_saludo("hidratacion")
    assert not es_saludo("heyyy")
    assert "hidratacion" in INFO


if __name__ == "__main__":
    test_saludos()
    test_temas_no_son_saludo()
    print("ok")
