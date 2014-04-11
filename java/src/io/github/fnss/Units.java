package io.github.fnss;

import java.util.HashMap;
import java.util.Map;

/**
 * Utility class providing methods and constants for units validation and
 * conversion
 * 
 * @author Lorenzo Saino
 */
public class Units {

	public static final String CAPACITY_GIGABIT_PER_SEC = "Gbps";
	public static final String CAPACITY_MEGABIT_PER_SEC = "Mbps";
	public static final String CAPACITY_KILOBIT_PER_SEC = "kbps";
	public static final String CAPACITY_BIT_PER_SEC = "bps";

	public static final String DELAY_NANOSECONDS = "ns";
	public static final String DELAY_MICROSECONDS = "us";
	public static final String DELAY_MILLISECONDS = "ms";
	public static final String DELAY_SECONDS = "sec";

	public static final String TIME_MICROSECONDS = "us";
	public static final String TIME_MILLISECONDS = "ms";
	public static final String TIME_SECONDS = "sec";
	public static final String TIME_MINUTES = "min";
	
	public static final String DISTANCE_METERS = "m";
	public static final String DISTANCE_KILOMETERS = "km";
	
	public static final String BUFFER_SIZE_BYTES = "bytes";
	public static final String BUFFER_SIZE_PACKETS = "packets";
	
	private static Map<String, Integer> timeUnitMap = 
			new HashMap<String, Integer>();
	private static Map<String, Integer> delayUnitMap = 
			new HashMap<String, Integer>();
	private static Map<String, Integer> capacityUnitMap = 
			new HashMap<String, Integer>();
	private static Map<String, Integer> distanceUnitMap = 
			new HashMap<String, Integer>();
	
	static {
		timeUnitMap.put(TIME_MICROSECONDS, 1);
		timeUnitMap.put(TIME_MILLISECONDS, 1000);
		timeUnitMap.put(TIME_SECONDS, 1000000);
		timeUnitMap.put(TIME_MINUTES, 60000000);
		
		delayUnitMap.put(DELAY_NANOSECONDS, 1);
		delayUnitMap.put(DELAY_MICROSECONDS, 1000);
		delayUnitMap.put(DELAY_MILLISECONDS, 1000000);
		delayUnitMap.put(DELAY_SECONDS, 1000000000);
		
		capacityUnitMap.put(CAPACITY_BIT_PER_SEC, 1);
		capacityUnitMap.put(CAPACITY_KILOBIT_PER_SEC, 1000);
		capacityUnitMap.put(CAPACITY_MEGABIT_PER_SEC, 1000000);
		capacityUnitMap.put(CAPACITY_GIGABIT_PER_SEC, 1000000000);

		distanceUnitMap.put(DISTANCE_METERS, 1);
		distanceUnitMap.put(DISTANCE_KILOMETERS, 1000);
	}
	
	// override scope of constructor to prevent instantiation
	private Units() { }
	
	/**
	 * Verify if the provided time unit is valid or not.
	 * 
	 * Valid time units are "us" (microseconds), "ms" (milliseconds), "sec"
	 * (seconds) and "min" (minutes).
	 * 
	 * @param timeUnit the time unit to be tested.
	 * @return <code>true</code> if the unit is valid, <code>false</code>
	 * otherwise
	 */
	public static boolean isValidTimeUnit(String timeUnit) {
		return timeUnitMap.get(timeUnit) == null ? false : true;
	}
	
	/**
	 * Verify if the provided delay unit is valid or not.
	 * 
	 * Valid time units are "ns" (nanoseconds), "us" (microseconds), "ms"
	 * (milliseconds), "sec" (seconds) and "min" (minutes).
	 * 
	 * @param delayUnit the delay unit to be tested.
	 * @return <code>true</code> if the unit is valid, <code>false</code>
	 * otherwise
	 */
	public static boolean isValidDelayUnit(String delayUnit) {
		return delayUnitMap.get(delayUnit) == null ? false : true;
	}

	/**
	 * Verify if the provided capacity unit is valid or not.
	 * 
	 * Valid time units are "bps" (bit per seconds), "Kbps" (Kbit per second),
	 * "Mbps" (Megabit per second), "Gbps" (Gigabit per seconds)
	 * 
	 * @param capacityUnit the capacity unit to be tested.
	 * @return <code>true</code> if the unit is valid, <code>false</code>
	 * otherwise
	 */
	public static boolean isValidCapacityUnit(String capacityUnit) {
		return capacityUnitMap.get(capacityUnit) == null ? false : true;
	}
	
	/**
	 * Verify if the provided capacity unit is valid or not.
	 * 
	 * Valid distance units are "m" (meters) and "Km" (kilometers)
	 * 
	 * @param distanceUnit the distance unit to be tested.
	 * @return <code>true</code> if the unit is valid, <code>false</code>
	 * otherwise
	 */
	public static boolean isValidDistanceUnit(String distanceUnit) {
		return distanceUnitMap.get(distanceUnit) == null ? false : true;
	}

	/**
	 * Verify if the provided buffer size unit is valid or not.
	 * 
	 * Valid time units are "bytes" or "packets"
	 * 
	 * @param bufferUnit the buffer unit to be tested.
	 * @return <code>true</code> if the unit is valid, <code>false</code>
	 * otherwise
	 */
	public static boolean isValidBufferUnit(String bufferUnit) {
		return bufferUnit.equals(BUFFER_SIZE_PACKETS)
				|| bufferUnit.equals(BUFFER_SIZE_BYTES);
	}

	/**
	 * Convert a time value from a time unit to another
	 * 
	 * @param value The time value to convert
	 * @param timeUnit the original time unit
	 * @param targetTimeUnit the target time unit
	 * 
	 * @return the time value expressed in the target unit
	 */
	public static float convertTimeValue(float value, String timeUnit,
			String targetTimeUnit) {
		if (timeUnitMap.get(timeUnit) == null) {
			throw new IllegalArgumentException(
					"The timeUnit parameter is invalid");
		}
		if (timeUnitMap.get(targetTimeUnit) == null) {
			throw new IllegalArgumentException(
					"The targetTimeUnit parameter is invalid");
		}
		float conversionFactor = timeUnitMap.get(timeUnit) /
				(float) timeUnitMap.get(targetTimeUnit);
		return value * conversionFactor;
	}

	/**
	 * Convert a delay value from a time unit to another
	 * 
	 * @param value The delay value to convert
	 * @param delayUnit the original delay unit
	 * @param targetDelayUnit the target delay unit
	 * 
	 * @return the delay value expressed in the target unit
	 */
	public static float convertDelayValue(float value, String delayUnit,
			String targetDelayUnit) {
		if (delayUnitMap.get(delayUnit) == null) {
			throw new IllegalArgumentException(
					"The delayUnit parameter is invalid");
		}
		if (delayUnitMap.get(targetDelayUnit) == null) {
			throw new IllegalArgumentException(
					"The targetDelayUnit parameter is invalid");
		}
		float conversionFactor = delayUnitMap.get(delayUnit)
				/ (float) delayUnitMap.get(targetDelayUnit);
		return value * conversionFactor;
	}

	/**
	 * Convert a capacity value from a time unit to another
	 * 
	 * @param value The capacity value to convert
	 * @param capacityUnit the original capacity unit
	 * @param targetCapacityUnit the target capacity unit
	 * 
	 * @return the capacity value expressed in the target unit
	 */
	public static float convertCapacityValue(float value,
			String capacityUnit, String targetCapacityUnit) {
		if (capacityUnitMap.get(capacityUnit) == null) {
			throw new IllegalArgumentException(
					"The capacityUnit parameter is invalid");
		}
		if (capacityUnitMap.get(targetCapacityUnit) == null) {
			throw new IllegalArgumentException(
					"The targetCapacityUnit parameter is invalid");
		}
		float conversionFactor = capacityUnitMap.get(capacityUnit)
				/ (float) capacityUnitMap.get(targetCapacityUnit);
		return value * conversionFactor;
	}

	/**
	 * Convert a distance value from a time unit to another
	 * 
	 * @param value The capacity value to convert
	 * @param distanceUnit the original distance unit
	 * @param targetDistanceUnit the target distance unit
	 * 
	 * @return the distance value expressed in the target unit
	 */
	public static float convertDistanceValue(float value,
			String distanceUnit, String targetDistanceUnit) {
		if (distanceUnitMap.get(distanceUnit) == null) {
			throw new IllegalArgumentException(
					"The distanceUnit parameter is invalid");
		}
		if (distanceUnitMap.get(targetDistanceUnit) == null) {
			throw new IllegalArgumentException(
					"The targetDistanceUnit parameter is invalid");
		}
		float conversionFactor = distanceUnitMap.get(distanceUnit)
				/ (float) distanceUnitMap.get(targetDistanceUnit);
		return value * conversionFactor;
	}
}
