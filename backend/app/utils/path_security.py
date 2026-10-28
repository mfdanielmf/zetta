LONGITUD_MAXIMA: int = 200


def sanear_nombre_archivo_zip(name: str | None) -> str:
    """
    Sanear nombres de archivos para usar dentro de ZIP
    """
    if not name:
        return "unnamed"

    # Bytes nulos.
    name = name.replace("\x00", "")

    name = name.replace("/", "_").replace("\\", "_")

    name = name.strip(". ")

    if not name or name == "." or name == "..":
        return "unnamed"

    if len(name) > LONGITUD_MAXIMA:
        name = name[:LONGITUD_MAXIMA].rsplit(".", 1)[0]
        if not name:
            name = "unnamed"

    return name
