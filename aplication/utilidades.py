import enum


def devolver_numero_paginas(total_registros,
                            numero_x_pagina=5):

    numero_de_paginas = total_registros // numero_x_pagina

    if total_registros % numero_x_pagina > 0:
        numero_de_paginas = numero_de_paginas + 1

    return numero_de_paginas


def devolver_lista_mayusculas():
    import string

    letras_mayusculas = []
    for l in string.ascii_uppercase:
        letras_mayusculas.append(l)
    return letras_mayusculas


class EstadoCita(enum.Enum):
    PENDIENTE = "Pendiente"
    FINALIZADA = "Finalizada"
    CANCELADA = "Cancelada"

    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        """item will be both type(enum) AND type(unicode).
        """
        if item == 'Pendiente' or item == EstadoCita.PENDIENTE:
            return EstadoCita.PENDIENTE
        elif item == 'Finalizada' or item == EstadoCita.FINALIZADA:
            return EstadoCita.FINALIZA
        elif item == 'Cancelada' or item == EstadoCita.CANCELADA:
            return EstadoCita.CANCELADA
        else:
            print
            "Can't coerce", item, type(item)

    @classmethod
    def from_name(cls, name):
        for estado, estado_name in EstadoCita.choices():
            if estado_name == name or name == str(estado):
                return estado
        raise ValueError('{} is not a valid EstadoCita name'.format(name))
