import { api } from './api';

export async function getDashboardData() {
  const [
    performanceResponse,
    timelineResponse,
    driftResponse,
    rootCauseResponse,
    modelHealthResponse,
    eventsResponse,
    businessResponse,
  ] = await Promise.all([
    api.get('/performance'),
    api.get('/performance/timeline'),
    api.get('/drift'),
    api.get('/root-cause'),
    api.get('/model-health'),
    api.get('/events'),
    api.get('/business-impact'),
  ]);

  return {
    performance: performanceResponse.data,
    timeline: timelineResponse.data,
    drift: driftResponse.data.features,
    rootCause: rootCauseResponse.data,
    modelHealth: modelHealthResponse.data,
    events: eventsResponse.data,
    business: businessResponse.data,
  };
}
