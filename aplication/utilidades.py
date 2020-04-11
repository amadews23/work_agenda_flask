import enum


def lista_letras_mayusculas():
    lista_letras_mayusculas=["A", "B", "C", "D", "E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

    return lista_letras_mayusculas

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
