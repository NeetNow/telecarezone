import React from 'react';
import { Card } from '@/components/ui/card';

export default function PrivacyPolicy() {
  return (
    <div className="min-h-screen bg-gray-50">
      <section className="py-20 px-6 bg-gradient-to-r from-purple-600 to-blue-500 text-white">
        <div className="container mx-auto max-w-4xl text-center">
          <h1 className="text-5xl font-bold mb-6">Privacy Policy</h1>
          <p className="text-xl opacity-90">Last updated: January 5, 2026</p>
        </div>
      </section>

      <div className="container mx-auto max-w-4xl px-6 py-16">
        <Card className="p-8 prose prose-lg max-w-none">
          <h2>1. Information We Collect</h2>
          <p>
            We collect information that you provide directly to us, including:
          </p>
          <ul>
            <li>Personal information (name, email, phone number)</li>
            <li>Medical history and health information</li>
            <li>Payment information</li>
            <li>Consultation records and prescriptions</li>
          </ul>

          <h2>2. How We Use Your Information</h2>
          <p>We use the collected information to:</p>
          <ul>
            <li>Provide and improve our telemedicine services</li>
            <li>Process appointments and payments</li>
            <li>Communicate with you about consultations</li>
            <li>Ensure the security of our platform</li>
            <li>Comply with legal obligations</li>
          </ul>

          <h2>3. Data Security</h2>
          <p>
            We implement industry-standard security measures to protect your personal
            and medical information. All data is encrypted during transmission and storage.
          </p>

          <h2>4. Sharing of Information</h2>
          <p>We do not sell your personal information. We may share your data with:</p>
          <ul>
            <li>Healthcare professionals for consultation purposes</li>
            <li>Payment processors for transaction processing</li>
            <li>Law enforcement when required by law</li>
          </ul>

          <h2>5. Your Rights</h2>
          <p>You have the right to:</p>
          <ul>
            <li>Access your personal information</li>
            <li>Request correction of inaccurate data</li>
            <li>Request deletion of your account</li>
            <li>Opt-out of marketing communications</li>
          </ul>

          <h2>6. Cookies and Tracking</h2>
          <p>
            We use cookies and similar technologies to improve user experience and
            analyze platform usage. You can control cookies through your browser settings.
          </p>

          <h2>7. Children's Privacy</h2>
          <p>
            Our services are not intended for individuals under 18 years of age.
            Consultations for minors require parental consent.
          </p>

          <h2>8. Changes to Privacy Policy</h2>
          <p>
            We may update this policy periodically. Users will be notified of significant
            changes via email or platform notification.
          </p>

          <h2>9. Contact Us</h2>
          <p>
            For privacy-related inquiries, contact us at:
            <br />
            Email: privacy@telecarezone.com
            <br />
            Phone: +91 1800-XXX-XXXX
          </p>
        </Card>
      </div>
    </div>
  );
}