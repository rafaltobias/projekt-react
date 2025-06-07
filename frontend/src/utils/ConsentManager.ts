/**
 * Consent Manager - Manages user consent for data tracking
 */

export interface ConsentStatus {
  granted: boolean;
  timestamp: string;
  hasDecision: boolean;
}

class ConsentManager {
  private static readonly CONSENT_KEY = 'data_sharing_consent';
  private static readonly TIMESTAMP_KEY = 'consent_timestamp';

  /**
   * Check if user has given consent for data tracking
   */
  static hasConsent(): boolean {
    const consent = localStorage.getItem(this.CONSENT_KEY);
    return consent === 'granted';
  }

  /**
   * Check if user has already made a consent decision
   */
  static hasConsentDecision(): boolean {
    const consent = localStorage.getItem(this.CONSENT_KEY);
    return consent !== null && (consent === 'granted' || consent === 'denied');
  }

  /**
   * Get full consent status
   */
  static getConsentStatus(): ConsentStatus {
    const consent = localStorage.getItem(this.CONSENT_KEY);
    const timestamp = localStorage.getItem(this.TIMESTAMP_KEY);
    
    return {
      granted: consent === 'granted',
      timestamp: timestamp || '',
      hasDecision: consent !== null
    };
  }

  /**
   * Grant consent for data tracking
   */
  static grantConsent(): void {
    localStorage.setItem(this.CONSENT_KEY, 'granted');
    localStorage.setItem(this.TIMESTAMP_KEY, new Date().toISOString());
  }

  /**
   * Deny consent for data tracking
   */
  static denyConsent(): void {
    localStorage.setItem(this.CONSENT_KEY, 'denied');
    localStorage.setItem(this.TIMESTAMP_KEY, new Date().toISOString());
  }

  /**
   * Clear consent decision (user can decide again)
   */
  static clearConsent(): void {
    localStorage.removeItem(this.CONSENT_KEY);
    localStorage.removeItem(this.TIMESTAMP_KEY);
  }

  /**
   * Check if consent is required (no decision made yet)
   */
  static isConsentRequired(): boolean {
    return !this.hasConsentDecision();
  }

  /**
   * Get consent timestamp
   */
  static getConsentTimestamp(): Date | null {
    const timestamp = localStorage.getItem(this.TIMESTAMP_KEY);
    return timestamp ? new Date(timestamp) : null;
  }

  /**
   * Check if consent was granted in the last N days
   */
  static isConsentFresh(days: number = 365): boolean {
    const timestamp = this.getConsentTimestamp();
    if (!timestamp || !this.hasConsent()) {
      return false;
    }

    const daysDiff = (Date.now() - timestamp.getTime()) / (1000 * 60 * 60 * 24);
    return daysDiff <= days;
  }
}

export default ConsentManager;
