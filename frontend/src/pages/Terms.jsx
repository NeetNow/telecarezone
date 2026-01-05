import React from 'react';
import { Card } from '@/components/ui/card';

export default function Terms() {
  return (
    <div className="min-h-screen bg-gray-50">
      <section className="py-20 px-6 bg-gradient-to-r from-purple-600 to-blue-500 text-white">
        <div className="container mx-auto max-w-4xl text-center">
          <h1 className="text-5xl font-bold mb-6">Terms of Service</h1>
          <p className="text-xl opacity-90">Last updated: January 5, 2026</p>
        </div>
      </section>

      <div className="container mx-auto max-w-4xl px-6 py-16">
        <Card className="p-8 prose prose-lg max-w-none">
          <h2>1. Acceptance of Terms</h2>
          <p>
            By accessing and using TeleCareZone platform, you accept and agree to be
            bound by the terms and provisions of this agreement.
          </p>

          <h2>2. Service Description</h2>
          <p>
            TeleCareZone provides a platform connecting patients with licensed healthcare
            professionals for virtual consultations. We do not practice medicine or provide
            medical advice directly.
          </p>

          <h2>3. User Responsibilities</h2>
          <p>As a user, you agree to:</p>
          <ul>
            <li>Provide accurate and complete information</li>
            <li>Maintain the confidentiality of your account</li>
            <li>Use the platform only for lawful purposes</li>
            <li>Follow medical advice provided by healthcare professionals</li>
            <li>Pay all applicable fees for services</li>
          </ul>

          <h2>4. Healthcare Professional Verification</h2>
          <p>
            We verify the credentials of healthcare professionals on our platform.
            However, users should independently verify qualifications when making
            healthcare decisions.
          </p>

          <h2>5. Medical Disclaimer</h2>
          <p>
            Teleconsultations have limitations. In case of emergencies, contact local
            emergency services immediately. The platform is not a substitute for
            in-person medical care when required.
          </p>

          <h2>6. Payment Terms</h2>
          <ul>
            <li>All fees must be paid before consultation</li>
            <li>Refunds are subject to our refund policy</li>
            <li>Failed or cancelled appointments may be charged</li>
          </ul>

          <h2>7. Intellectual Property</h2>
          <p>
            All content on the platform, including text, graphics, logos, and software,
            is the property of TeleCareZone and protected by copyright laws.
          </p>

          <h2>8. Limitation of Liability</h2>
          <p>
            TeleCareZone is not liable for any direct, indirect, or consequential damages
            arising from the use of our platform or services provided by healthcare
            professionals.
          </p>

          <h2>9. Termination</h2>
          <p>
            We reserve the right to terminate or suspend access to our platform for
            violation of these terms or any unlawful activity.
          </p>

          <h2>10. Governing Law</h2>
          <p>
            These terms shall be governed by and construed in accordance with the laws
            of India. Disputes shall be subject to the jurisdiction of Mumbai courts.
          </p>

          <h2>11. Contact Information</h2>
          <p>
            For questions about these terms, contact:
            <br />
            Email: legal@mykitchenfarm.com
            <br />
            Phone: +91 1800-XXX-XXXX
          </p>
        </Card>
      </div>
    </div>
  );
}