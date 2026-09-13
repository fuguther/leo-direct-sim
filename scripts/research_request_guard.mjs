/** Harness llm/stream waterfall adapter.
 * Broker must enforce authorization, route attestation and durable reservation.
 * No broker is bundled for live use yet: bound sessions fail closed.
 */
import { randomUUID } from 'node:crypto';
export const name = 'research-request-guard';
export const inject = ['researchBudgetBroker'];

export function apply(ctx) {
  const broker = ctx.get('researchBudgetBroker');
  if (!broker) throw new Error('RESEARCH_BUDGET_BROKER_MISSING');
  ctx.on('llm/stream', async function* (options, next) {
    // Binding lookup must distinguish unbound from unavailable; errors propagate.
    const binding = await broker.binding(options.sessionId);
    if (!binding) {
      yield* await next();
      return;
    }
    if (!options.sessionId) throw new Error('BOUND_REQUEST_WITHOUT_SESSION');
    if (options.signal?.aborted) throw new Error('RESEARCH_CANCELLED');
    const requestId = randomUUID(); // Each retry must reserve separately.
    const permit = await broker.reserve({ requestId, sessionId: options.sessionId,
      provider: options.provider, model: options.model,
      maxTokens: options.maxTokens, purpose: options.purpose ?? 'generation' });
    if (!permit || permit.requestId !== requestId || permit.routeAttested !== true ||
        permit.costBoundVerified !== true) throw new Error('RESEARCH_PERMIT_INVALID');
    let complete = false;
    try {
      // Recheck stop after reservation and immediately before the adapter.
      await broker.beforeDispatch(requestId);
      if (options.signal?.aborted) throw new Error('RESEARCH_CANCELLED');
      for await (const chunk of await next()) {
        // Charge and reconcile before reporting completion to the caller.
        if (chunk.type === 'finish') {
          await broker.finish(requestId, chunk);
          complete = true;
        }
        yield chunk;
      }
    } finally {
      // Unknown response/consumer cancellation never releases the reservation.
      if (!complete) await broker.uncertain(requestId);
    }
  });
}
