/**
 * Test Fixture: Unused Imports Vulnerable Pattern (TypeScript)
 *
 * This file contains import statements that are never used.
 * Expected detections: >=1 violation for AP-007
 * Rule ID: AP-007
 * Severity: MEDIUM (info)
 */

import { useState, useEffect } from 'react';  // useEffect UNUSED - VULNERABLE
import * as lodash from 'lodash';              // UNUSED - VULNERABLE
import axios from 'axios';                     // UNUSED - VULNERABLE

export function MyComponent(): void {
  const [count, setCount] = useState(0);  // Only useState is used
  setCount(count + 1);
}
