package com.analytics.platform.strategy;

import java.util.Map;

/** Strategy abstraction for interchangeable analytics workloads. */
public interface ProcessingStrategy { String key(); Map<String, Object> process(Map<String, Object> parameters); }
