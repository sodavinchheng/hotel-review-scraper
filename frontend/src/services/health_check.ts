import { healthApi } from "@/core/http/openAPIClient";
import type { HealthCheck } from "@/types/domain";

export class HealthCheckService {
  private static instance: HealthCheckService;

  private constructor() {}

  public static getInstance(): HealthCheckService {
    if (!HealthCheckService.instance) {
      HealthCheckService.instance = new HealthCheckService();
    }

    return HealthCheckService.instance;
  }

  public static async check(): Promise<HealthCheck> {
    try {
      const response = await healthApi.healthCheckApiHealthGet();
      return response.data;
    } catch (error) {
      console.error("Error fetching HealthChecks:", error);
      throw error;
    }
  }
}
