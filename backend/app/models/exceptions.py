# AUTH
class NombreYaUsadoException(Exception):
    pass


class CorreoYaUsadoException(Exception):
    pass


class UsuarioNoAutenticadoException(Exception):
    pass


# USUARIOS
class UsuarioNoEncontradoException(Exception):
    pass


class ContraseñaIncorrectaException(Exception):
    pass


# ARCHIVOS
class TamañoExcedidoException(Exception):
    pass


class ArchivoNoEncontradoException(Exception):
    pass


class ArchivoPapeleraException(Exception):
    pass


# CARPETAS
class CarpetaNoEncontradaException(Exception):
    pass


class CarpetaPapeleraException(Exception):
    pass


# GENERAL
class IdYaUsadaException(Exception):
    pass


class NombreYaUsadoException(Exception):
    pass
