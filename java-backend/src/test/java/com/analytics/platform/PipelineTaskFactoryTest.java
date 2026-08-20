package com.analytics.platform;

import com.analytics.platform.factory.PipelineTaskFactory;
import com.analytics.platform.strategy.*;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class PipelineTaskFactoryTest {
    @Test void resolvesKnownStrategyAndRejectsUnknown() { var factory = new PipelineTaskFactory(List.of(new AnomalyDetectionStrategy(), new ForecastingStrategy())); assertEquals("anomaly-detection", factory.resolve("anomaly-detection").key()); assertThrows(IllegalArgumentException.class, () -> factory.resolve("unknown")); }
}
