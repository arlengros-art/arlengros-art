import { describe, it, expect } from 'vitest';
import { generate } from '../src/api';

describe('generate', () => {
  it('returns ok', () => {
    expect(generate()).toBe('ok');
  });
});
