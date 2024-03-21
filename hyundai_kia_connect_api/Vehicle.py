# pylint:disable=missing-class-docstring,missing-function-docstring,wildcard-import,unused-wildcard-import,invalid-name
"""Vehicle class"""
import logging
import datetime
import typing
from dataclasses import dataclass, field

from .utils import get_child_value, get_float, parse_datetime
from .const import *

_LOGGER = logging.getLogger(__name__)


@dataclass
class TripInfo:
    """Trip Info"""

    hhmmss: str = None  # will not be filled by summary
    drive_time: int = None
    idle_time: int = None
    distance: int = None
    avg_speed: float = None
    max_speed: int = None


@dataclass
class DayTripCounts:
    """Day trip counts"""

    yyyymmdd: str = None
    trip_count: int = None


@dataclass
class MonthTripInfo:
    """Month Trip Info"""

    yyyymm: str = None
    summary: TripInfo = None
    day_list: list[DayTripCounts] = field(default_factory=list)


@dataclass
class DayTripInfo:
    """Day Trip Info"""

    yyyymmdd: str = None
    summary: TripInfo = None
    trip_list: list[TripInfo] = field(default_factory=list)


@dataclass
class DailyDrivingStats:
    # energy stats are expressed in watthours (Wh)
    date: datetime.datetime = None
    total_consumed: int = None
    engine_consumption: int = None
    climate_consumption: int = None
    onboard_electronics_consumption: int = None
    battery_care_consumption: int = None
    regenerated_energy: int = None
    # distance is expressed in (I assume) whatever unit the vehicle is
    # configured in. KMs (rounded) in my case
    distance: int = None
    distance_unit = DISTANCE_UNITS[1]  # set to kms by default


@dataclass
class Vehicle:
    id: str = None
    name: str = None
    model: str = None
    registration_date: str = None
    year: int = None
    VIN: str = None
    key: str = None
    ccu_ccs2_protocol_support: int = None
    # Not part of the API, enabled in our library for scanning.
    enabled: bool = True

    # Shared (EV/PHEV/HEV/IC)
    # General
    _total_driving_range: float = None
    _total_driving_range_value: float = None
    _total_driving_range_unit: str = None

    _odometer: float = None
    _odometer_value: float = None
    _odometer_unit: str = None

    _geocode_address: str = None
    _geocode_name: str = None

    car_battery_percentage: int = None
    engine_is_running: bool = None
    last_updated_at: datetime.datetime = None
    timezone: datetime.timezone = datetime.timezone.utc  # default UTC
    dtc_count: typing.Union[int, None] = None
    dtc_descriptions: typing.Union[dict, None] = None

    smart_key_battery_warning_is_on: bool = None
    washer_fluid_warning_is_on: bool = None
    brake_fluid_warning_is_on: bool = None

    # Climate
    _air_temperature: float = None
    _air_temperature_value: float = None
    _air_temperature_unit: str = None

    air_control_is_on: bool = None
    defrost_is_on: bool = None
    steering_wheel_heater_is_on: bool = None
    back_window_heater_is_on: bool = None
    side_mirror_heater_is_on: bool = None
    front_left_seat_status: str = None
    front_right_seat_status: str = None
    rear_left_seat_status: str = None
    rear_right_seat_status: str = None

    # Door Status
    is_locked: bool = None
    front_left_door_is_open: bool = None
    front_right_door_is_open: bool = None
    back_left_door_is_open: bool = None
    back_right_door_is_open: bool = None
    trunk_is_open: bool = None
    hood_is_open: bool = None

    # Window Status
    front_left_window_is_open: bool = None
    front_right_window_is_open: bool = None
    back_left_window_is_open: bool = None
    back_right_window_is_open: bool = None

    # Tire Pressure
    tire_pressure_all_warning_is_on: bool = None
    tire_pressure_rear_left_warning_is_on: bool = None
    tire_pressure_front_left_warning_is_on: bool = None
    tire_pressure_front_right_warning_is_on: bool = None
    tire_pressure_rear_right_warning_is_on: bool = None

    # Service Data
    _next_service_distance: float = None
    _next_service_distance_value: float = None
    _next_service_distance_unit: str = None
    _last_service_distance: float = None
    _last_service_distance_value: float = None
    _last_service_distance_unit: str = None

    # Location
    _location_latitude: float = None
    _location_longitude: float = None
    _location_last_set_time: datetime.datetime = None

    # EV fields (EV/PHEV)

    ev_charge_port_door_is_open: typing.Union[bool, None] = None

    ev_charge_limits_dc: typing.Union[int, None] = None
    ev_charge_limits_ac: typing.Union[int, None] = None
    ev_v2l_discharge_limit: typing.Union[int, None] = None

    # energy consumed and regenerated since the vehicle was paired with the account
    # (so not necessarily for the vehicle's lifetime)
    # expressed in watt-hours (Wh)
    total_power_consumed: float = None  # Europe feature only
    total_power_regenerated: float = None  # Europe feature only
    # energy consumed in the last ~30 days
    # expressed in watt-hours (Wh)
    power_consumption_30d: float = None  # Europe feature only

    # Europe feature only
    daily_stats: list[DailyDrivingStats] = field(default_factory=list)

    month_trip_info: MonthTripInfo = None  # Europe feature only
    day_trip_info: DayTripInfo = None  # Europe feature only

    ev_battery_percentage: int = None
    ev_battery_soh_percentage: int = None
    ev_battery_remain: int = None
    ev_battery_capacity: int = None
    ev_battery_is_charging: bool = None
    ev_battery_is_plugged_in: bool = None

    _ev_driving_range: float = None
    _ev_driving_range_value: float = None
    _ev_driving_range_unit: str = None

    _ev_estimated_current_charge_duration: int = None
    _ev_estimated_current_charge_duration_value: int = None
    _ev_estimated_current_charge_duration_unit: str = None

    _ev_estimated_fast_charge_duration: int = None
    _ev_estimated_fast_charge_duration_value: int = None
    _ev_estimated_fast_charge_duration_unit: str = None

    _ev_estimated_portable_charge_duration: int = None
    _ev_estimated_portable_charge_duration_value: int = None
    _ev_estimated_portable_charge_duration_unit: str = None

    _ev_estimated_station_charge_duration: int = None
    _ev_estimated_station_charge_duration_value: int = None
    _ev_estimated_station_charge_duration_unit: str = None

    _ev_target_range_charge_AC: typing.Union[float, None] = None
    _ev_target_range_charge_AC_value: typing.Union[float, None] = None
    _ev_target_range_charge_AC_unit: typing.Union[str, None] = None

    _ev_target_range_charge_DC: typing.Union[float, None] = None
    _ev_target_range_charge_DC_value: typing.Union[float, None] = None
    _ev_target_range_charge_DC_unit: typing.Union[str, None] = None

    ev_first_departure_enabled: typing.Union[bool, None] = None
    ev_second_departure_enabled: typing.Union[bool, None] = None

    ev_first_departure_days: typing.Union[list, None] = None
    ev_second_departure_days: typing.Union[list, None] = None

    ev_first_departure_time: typing.Union[datetime.time, None] = None
    ev_second_departure_time: typing.Union[datetime.time, None] = None

    ev_off_peak_start_time: typing.Union[datetime.time, None] = None
    ev_off_peak_end_time: typing.Union[datetime.time, None] = None
    ev_off_peak_charge_only_enabled: typing.Union[bool, None] = None

    # IC fields (PHEV/HEV/IC)
    _fuel_driving_range: float = None
    _fuel_driving_range_value: float = None
    _fuel_driving_range_unit: str = None
    fuel_level: float = None

    fuel_level_is_low: bool = None

    # Calculated fields
    engine_type: str = None

    # Debug fields
    data: dict = None

    @property
    def geocode(self):
        return self._geocode_name, self._geocode_address

    @geocode.setter
    def geocode(self, value):
        self._geocode_name = value[0]
        self._geocode_address = value[1]

    @property
    def total_driving_range(self):
        return self._total_driving_range

    @property
    def total_driving_range_unit(self):
        return self._total_driving_range_unit

    @total_driving_range.setter
    def total_driving_range(self, value):
        self._total_driving_range_value = value[0]
        self._total_driving_range_unit = value[1]
        self._total_driving_range = value[0]

    @property
    def next_service_distance(self):
        return self._next_service_distance

    @next_service_distance.setter
    def next_service_distance(self, value):
        self._next_service_distance_value = value[0]
        self._next_service_distance_unit = value[1]
        self._next_service_distance = value[0]

    @property
    def last_service_distance(self):
        return self._last_service_distance

    @last_service_distance.setter
    def last_service_distance(self, value):
        self._last_service_distance_value = value[0]
        self._last_service_distance_unit = value[1]
        self._last_service_distance = value[0]

    @property
    def location_latitude(self):
        return self._location_latitude

    @property
    def location_longitude(self):
        return self._location_longitude

    @property
    def location(self):
        return self._location_longitude, self._location_latitude

    @property
    def location_last_updated_at(self):
        """
        return last location datetime.
        last_updated_at and location_last_updated_at can be different.
        The newest of those 2 can be computed by the caller.
        """
        return self._location_last_set_time

    @location.setter
    def location(self, value):
        self._location_latitude = value[0]
        self._location_longitude = value[1]
        self._location_last_set_time = value[2]

    @property
    def odometer(self):
        return self._odometer

    @property
    def odometer_unit(self):
        return self._odometer_unit

    @odometer.setter
    def odometer(self, value):
        float_value = get_float(value[0])
        self._odometer_value = float_value
        self._odometer_unit = value[1]
        self._odometer = float_value

    @property
    def air_temperature(self):
        return self._air_temperature

    @air_temperature.setter
    def air_temperature(self, value):
        self._air_temperature_value = value[0]
        self._air_temperature_unit = value[1]
        self._air_temperature = value[0]

    @property
    def ev_driving_range(self):
        return self._ev_driving_range

    @property
    def ev_driving_range_unit(self):
        return self._ev_driving_range_unit

    @ev_driving_range.setter
    def ev_driving_range(self, value):
        self._ev_driving_range_value = value[0]
        self._ev_driving_range_unit = value[1]
        self._ev_driving_range = value[0]

    @property
    def ev_estimated_current_charge_duration(self):
        return self._ev_estimated_current_charge_duration

    @ev_estimated_current_charge_duration.setter
    def ev_estimated_current_charge_duration(self, value):
        self._ev_estimated_current_charge_duration_value = value[0]
        self._ev_estimated_current_charge_duration_unit = value[1]
        self._ev_estimated_current_charge_duration = value[0]

    @property
    def ev_estimated_fast_charge_duration(self):
        return self._ev_estimated_fast_charge_duration

    @ev_estimated_fast_charge_duration.setter
    def ev_estimated_fast_charge_duration(self, value):
        self._ev_estimated_fast_charge_duration_value = value[0]
        self._ev_estimated_fast_charge_duration_unit = value[1]
        self._ev_estimated_fast_charge_duration = value[0]

    @property
    def ev_estimated_portable_charge_duration(self):
        return self._ev_estimated_portable_charge_duration

    @ev_estimated_portable_charge_duration.setter
    def ev_estimated_portable_charge_duration(self, value):
        self._ev_estimated_portable_charge_duration_value = value[0]
        self._ev_estimated_portable_charge_duration_unit = value[1]
        self._ev_estimated_portable_charge_duration = value[0]

    @property
    def ev_estimated_station_charge_duration(self):
        return self._ev_estimated_station_charge_duration

    @ev_estimated_station_charge_duration.setter
    def ev_estimated_station_charge_duration(self, value):
        self._ev_estimated_station_charge_duration_value = value[0]
        self._ev_estimated_station_charge_duration_unit = value[1]
        self._ev_estimated_station_charge_duration = value[0]

    @property
    def ev_target_range_charge_AC(self):
        return self._ev_target_range_charge_AC

    @property
    def ev_target_range_charge_AC_unit(self):
        return self._ev_target_range_charge_AC_unit

    @ev_target_range_charge_AC.setter
    def ev_target_range_charge_AC(self, value):
        self._ev_target_range_charge_AC_value = value[0]
        self._ev_target_range_charge_AC_unit = value[1]
        self._ev_target_range_charge_AC = value[0]

    @property
    def ev_target_range_charge_DC(self):
        return self._ev_target_range_charge_DC

    @property
    def ev_target_range_charge_DC_unit(self):
        return self._ev_target_range_charge_DC_unit

    @ev_target_range_charge_DC.setter
    def ev_target_range_charge_DC(self, value):
        self._ev_target_range_charge_DC_value = value[0]
        self._ev_target_range_charge_DC_unit = value[1]
        self._ev_target_range_charge_DC = value[0]

    @property
    def fuel_driving_range(self):
        return self._fuel_driving_range

    @fuel_driving_range.setter
    def fuel_driving_range(self, value):
        self._fuel_driving_range_value = value[0]
        self._fuel_driving_range_unit = value[1]
        self._fuel_driving_range = value[0]

    def update_ccs2(self, timezone: datetime.tzinfo, state: dict):
        if get_child_value(state, "Date"):
            self.last_updated_at = parse_datetime(
                get_child_value(state, "Date"), timezone
            )
        else:
            self.last_updated_at = datetime.datetime.now(timezone)

        self.odometer = (
            get_child_value(state, "Drivetrain.Odometer"),
            DISTANCE_UNITS[1],
        )
        self.car_battery_percentage = get_child_value(
            state, "Electronics.Battery.Level"
        )

        self.engine_is_running = get_child_value(state, "DrivingReady")

        air_temp = get_child_value(
            state,
            "Cabin.HVAC.Row1.Driver.Temperature.Value",
        )

        if air_temp != "OFF":
            self.air_temperature = (air_temp, TEMPERATURE_UNITS[1])

        defrost_is_on = get_child_value(state, "Body.Windshield.Front.Defog.State")
        if defrost_is_on in [0, 2]:
            self.defrost_is_on = False
        elif defrost_is_on == 1:
            self.defrost_is_on = True

        steer_wheel_heat = get_child_value(state, "Cabin.SteeringWheel.Heat.State")
        if steer_wheel_heat in [0, 2]:
            self.steering_wheel_heater_is_on = False
        elif steer_wheel_heat == 1:
            self.steering_wheel_heater_is_on = True

        defrost_rear_is_on = get_child_value(state, "Body.Windshield.Rear.Defog.State")
        if defrost_rear_is_on in [0, 2]:
            self.back_window_heater_is_on = False
        elif defrost_rear_is_on == 1:
            self.back_window_heater_is_on = True

        # TODO: status.sideMirrorHeat

        self.front_left_seat_status = SEAT_STATUS[
            get_child_value(state, "Cabin.Seat.Row1.Driver.Climate.State")
        ]

        self.front_right_seat_status = SEAT_STATUS[
            get_child_value(state, "Cabin.Seat.Row1.Passenger.Climate.State")
        ]

        self.rear_left_seat_status = SEAT_STATUS[
            get_child_value(state, "Cabin.Seat.Row2.Left.Climate.State")
        ]

        self.rear_right_seat_status = SEAT_STATUS[
            get_child_value(state, "Cabin.Seat.Row2.Right.Climate.State")
        ]

        # TODO: status.doorLock

        self.front_left_door_is_open = get_child_value(
            state, "Cabin.Door.Row1.Driver.Open"
        )
        self.front_right_door_is_open = get_child_value(
            state, "Cabin.Door.Row1.Passenger.Open"
        )
        self.back_left_door_is_open = get_child_value(
            state, "Cabin.Door.Row2.Left.Open"
        )
        self.back_right_door_is_open = get_child_value(
            state, "Cabin.Door.Row2.Right.Open"
        )

        # TODO: should the windows and trunc also be checked?
        self.is_locked = not (
            self.front_left_door_is_open
            or self.front_right_door_is_open
            or self.back_left_door_is_open
            or self.back_right_door_is_open
        )

        self.hood_is_open = get_child_value(state, "Body.Hood.Open")
        self.front_left_window_is_open = get_child_value(
            state, "Cabin.Window.Row1.Driver.Open"
        )
        self.front_right_window_is_open = get_child_value(
            state, "Cabin.Window.Row1.Passenger.Open"
        )
        self.back_left_window_is_open = get_child_value(
            state, "Cabin.Window.Row2.Left.Open"
        )
        self.back_right_window_is_open = get_child_value(
            state, "Cabin.Window.Row2.Right.Open"
        )
        self.tire_pressure_rear_left_warning_is_on = bool(
            get_child_value(state, "Chassis.Axle.Row2.Left.Tire.PressureLow")
        )
        self.tire_pressure_front_left_warning_is_on = bool(
            get_child_value(state, "Chassis.Axle.Row1.Left.Tire.PressureLow")
        )
        self.tire_pressure_front_right_warning_is_on = bool(
            get_child_value(state, "Chassis.Axle.Row1.Right.Tire.PressureLow")
        )
        self.tire_pressure_rear_right_warning_is_on = bool(
            get_child_value(state, "Chassis.Axle.Row2.Right.Tire.PressureLow")
        )
        self.tire_pressure_all_warning_is_on = bool(
            get_child_value(state, "Chassis.Axle.Tire.PressureLow")
        )
        self.trunk_is_open = get_child_value(state, "Body.Trunk.Open")

        self.ev_battery_percentage = get_child_value(
            state, "Green.BatteryManagement.BatteryRemain.Ratio"
        )
        self.ev_battery_remain = get_child_value(
            state, "Green.BatteryManagement.BatteryRemain.Value"
        )
        self.ev_battery_capacity = get_child_value(
            state, "Green.BatteryManagement.BatteryCapacity.Value"
        )
        self.ev_battery_soh_percentage = get_child_value(
            state, "Green.BatteryManagement.SoH.Ratio"
        )
        self.ev_battery_is_plugged_in = get_child_value(
            state, "Green.ChargingInformation.ElectricCurrentLevel.State"
        )
        self.ev_battery_is_plugged_in = get_child_value(
            state, "Green.ChargingInformation.ConnectorFastening.State"
        )
        charging_door_state = get_child_value(state, "Green.ChargingDoor.State")
        if charging_door_state in [0, 2]:
            self.ev_charge_port_door_is_open = False
        elif charging_door_state == 1:
            self.ev_charge_port_door_is_open = True

        self.total_driving_range = (
            float(
                get_child_value(
                    state,
                    "Drivetrain.FuelSystem.DTE.Total",  # noqa
                )
            ),
            DISTANCE_UNITS[
                get_child_value(
                    state,
                    "Drivetrain.FuelSystem.DTE.Unit",  # noqa
                )
            ],
        )

        if self.engine_type == ENGINE_TYPES.EV:
            # ev_driving_range is the same as total_driving_range for pure EV
            self.ev_driving_range = (
                self.total_driving_range,
                self.total_driving_range_unit,
            )
        # TODO: self.ev_driving_range for non EV

        self.washer_fluid_warning_is_on = get_child_value(
            state, "Body.Windshield.Front.WasherFluid.LevelLow"
        )

        self.ev_estimated_current_charge_duration = (
            get_child_value(state, "Green.ChargingInformation.Charging.RemainTime"),
            "m",
        )
        self.ev_estimated_fast_charge_duration = (
            get_child_value(state, "Green.ChargingInformation.EstimatedTime.Standard"),
            "m",
        )
        self.ev_estimated_portable_charge_duration = (
            get_child_value(state, "Green.ChargingInformation.EstimatedTime.ICCB"),
            "m",
        )
        self.ev_estimated_station_charge_duration = (
            get_child_value(state, "Green.ChargingInformation.EstimatedTime.Quick"),
            "m",
        )
        self.ev_charge_limits_ac = get_child_value(
            state, "Green.ChargingInformation.TargetSoC.Standard"
        )
        self.ev_charge_limits_dc = get_child_value(
            state, "Green.ChargingInformation.TargetSoC.Quick"
        )
        self.ev_v2l_discharge_limit = get_child_value(
            state, "Green.Electric.SmartGrid.VehicleToLoad.DischargeLimitation.SoC"
        )
        self.ev_target_range_charge_AC = (
            get_child_value(
                state,
                "Green.ChargingInformation.DTE.TargetSoC.Standard",  # noqa
            ),
            DISTANCE_UNITS[
                get_child_value(
                    state,
                    "Drivetrain.FuelSystem.DTE.Unit",  # noqa
                )
            ],
        )
        self.ev_target_range_charge_DC = (
            get_child_value(
                state,
                "Green.ChargingInformation.DTE.TargetSoC.Quick",  # noqa
            ),
            DISTANCE_UNITS[
                get_child_value(
                    state,
                    "Drivetrain.FuelSystem.DTE.Unit",  # noqa
                )
            ],
        )
        self.ev_first_departure_enabled = bool(
            get_child_value(state, "Green.Reservation.Departure.Schedule1.Enable")
        )

        self.ev_second_departure_enabled = bool(
            get_child_value(state, "Green.Reservation.Departure.Schedule2.Enable")
        )

        # TODO: self.ev_first_departure_days --> Green.Reservation.Departure.Schedule1.(Mon,Tue,Wed,Thu,Fri,Sat,Sun) # noqa
        # TODO: self.ev_second_departure_days --> Green.Reservation.Departure.Schedule2.(Mon,Tue,Wed,Thu,Fri,Sat,Sun) # noqa
        # TODO: self.ev_first_departure_time --> Green.Reservation.Departure.Schedule1.(Min,Hour) # noqa
        # TODO: self.ev_second_departure_time --> Green.Reservation.Departure.Schedule2.(Min,Hour) # noqa
        # TODO: self.ev_off_peak_charge_only_enabled --> unknown settings are in  --> Green.Reservation.OffPeakTime and OffPeakTime2 # noqa

        self.washer_fluid_warning_is_on = get_child_value(
            state, "Body.Windshield.Front.WasherFluid.LevelLow"
        )
        self.brake_fluid_warning_is_on = get_child_value(
            state, "Chassis.Brake.Fluid.Warning"
        )

        self.fuel_level = get_child_value(state, "Drivetrain.FuelSystem.FuelLevel")
        self.fuel_level_is_low = get_child_value(
            state, "Drivetrain.FuelSystem.LowFuelWarning"
        )
        self.air_control_is_on = get_child_value(
            state, "Cabin.HVAC.Row1.Driver.Blower.SpeedLevel"
        )
        self.smart_key_battery_warning_is_on = bool(
            get_child_value(state, "Electronics.FOB.LowBattery")
        )

        if get_child_value(state, "Location.GeoCoord.Latitude"):
            location_last_updated_at = datetime.datetime(2000, 1, 1, tzinfo=timezone)
            timestamp = get_child_value(state, "Location.TimeStamp")
            if timestamp is not None:
                location_last_updated_at = datetime.datetime(
                    year=int(get_child_value(timestamp, "Year")),
                    month=int(get_child_value(timestamp, "Mon")),
                    day=int(get_child_value(timestamp, "Day")),
                    hour=int(get_child_value(timestamp, "Hour")),
                    minute=int(get_child_value(timestamp, "Min")),
                    second=int(get_child_value(timestamp, "Sec")),
                    tzinfo=timezone,
                )

            self.location = (
                get_child_value(state, "Location.GeoCoord.Latitude"),
                get_child_value(state, "Location.GeoCoord.Longitude"),
                location_last_updated_at,
            )

        self.data = state
