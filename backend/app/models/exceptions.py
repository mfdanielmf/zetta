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


# GENERAL
class IdYaUsadaException(Exception):
    pass
