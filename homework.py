M_IN_KM = 1000
HOURS_TO_MINUTES = 60
HEIGHT_TO_METERS = 100


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self, data) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        duration = data[1]
        distance = self.get_distance()
        speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        info = InfoMessage(training_type, duration, distance,
                           speed, spent_calories)
        print(info.get_message())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM
                * self.duration * HOURS_TO_MINUTES)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WALKING_CAL_KOEFF_1 = 0.035
    WALKING_CAL_KOEFF_2 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_spent_calories(self):
        return ((self.WALKING_CAL_KOEFF_1 * self.weight
                + (self.get_mean_speed() ** 2
                   / (self.height / HEIGHT_TO_METERS))
                * self.WALKING_CAL_KOEFF_2 * self.weight)
                * self.duration * HOURS_TO_MINUTES)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIM_CAL_COEF = 1.1
    SWIM_CAL_COEF_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self):
        return (self.get_mean_speed() + self.SWIM_CAL_COEF
                * self.SWIM_CAL_COEF_2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_workout = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return types_of_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    return training.show_training_info(data)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

for workout_type, data in packages:
    training = read_package(workout_type, data)
    main(training)
