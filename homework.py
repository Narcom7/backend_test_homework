from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Напечатать информацию о тернировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    AMAUNT_OF_MINUTES_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""


    CALLORIES_RUNING_MULTIPLICATION_FACTOR: float = 18
    CALLORIES_RUNING_SUBTRAHEND: float = 20


    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        expended_calories: float = ((
            self.CALLORIES_RUNING_MULTIPLICATION_FACTOR
            * self.get_mean_speed()
            - self.CALLORIES_RUNING_SUBTRAHEND)
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.AMAUNT_OF_MINUTES_IN_HOUR)
        return expended_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALLORIES_WEIGHT_MULTIPLICATION_FACTOR: float = 0.035
    CALLORIES_WEIGHT_MULTIPLICATION_FACTOR_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        expended_calories: float = ((
            self.CALLORIES_WEIGHT_MULTIPLICATION_FACTOR
            * self.weight
            + (self.get_mean_speed()**2
                // self.height)
            * self.CALLORIES_WEIGHT_MULTIPLICATION_FACTOR_2
            * self.weight)
            * self.duration
            * self.AMAUNT_OF_MINUTES_IN_HOUR
        )
        return expended_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALLORIES_SPEED_ADDENDS_FACTOR: float = 1.1
    CALLORIES_SPEED_MULTIPLIER_FACTOR: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        get_mean_speed = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return get_mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        expended_calories: float = ((
            self.get_mean_speed()
            + self.CALLORIES_SPEED_ADDENDS_FACTOR)
            * self.CALLORIES_SPEED_MULTIPLIER_FACTOR
            * self.weight
        )
        return expended_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dic = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking}
    if not workout_dic.get(workout_type):
        raise KeyError('Неизвестный идентификатор спорта')
    else:
        return workout_dic[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1.5, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)