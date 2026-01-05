import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight, CheckCircle, Users, Calendar, Shield, Phone } from 'lucide-react';

export default function About() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50">
      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="container mx-auto max-w-4xl text-center">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-purple-600 to-blue-500 bg-clip-text text-transparent">
            About TeleCareZone
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            India's Leading Telemedicine Platform Connecting Patients with Verified Healthcare Professionals
          </p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 px-6 bg-white">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
              <p className="text-lg text-gray-600 mb-4">
                To make quality healthcare accessible to everyone, everywhere through innovative telemedicine solutions.
              </p>
              <p className="text-lg text-gray-600 mb-4">
                We connect patients with verified healthcare professionals for instant consultations, breaking down geographical barriers and making healthcare more affordable and convenient.
              </p>
              <div className="flex gap-4 mt-8">
                <Button onClick={() => navigate('/join-expert')} className="bg-purple-600">
                  Join as Professional
                </Button>
                <Button onClick={() => navigate('/')} variant="outline">
                  Book Consultation
                </Button>
              </div>
            </div>
            <div className="space-y-6">
              <div className="flex gap-4 items-start">
                <CheckCircle className="w-6 h-6 text-green-500 mt-1" />
                <div>
                  <h3 className="font-semibold text-lg mb-2">Verified Professionals</h3>
                  <p className="text-gray-600">All healthcare professionals are verified and licensed</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <Shield className="w-6 h-6 text-blue-500 mt-1" />
                <div>
                  <h3 className="font-semibold text-lg mb-2">Secure & Private</h3>
                  <p className="text-gray-600">Your medical data is encrypted and completely confidential</p>
                </div>
              </div>
              <div className="flex gap-4 items-start">
                <Phone className="w-6 h-6 text-purple-500 mt-1" />
                <div>
                  <h3 className="font-semibold text-lg mb-2">24/7 Available</h3>
                  <p className="text-gray-600">Connect with doctors anytime, anywhere</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-6">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">500+</div>
              <div className="text-gray-600">Healthcare Professionals</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">10,000+</div>
              <div className="text-gray-600">Happy Patients</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">50+</div>
              <div className="text-gray-600">Specializations</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">24/7</div>
              <div className="text-gray-600">Support Available</div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 px-6 bg-white">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-12">Our Core Values</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <Card className="p-6 text-center">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-3">Patient First</h3>
              <p className="text-gray-600">Every decision we make puts patient welfare at the center</p>
            </Card>
            <Card className="p-6 text-center">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-semibold mb-3">Privacy & Security</h3>
              <p className="text-gray-600">Your medical information is protected with bank-level encryption</p>
            </Card>
            <Card className="p-6 text-center">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-3">Innovation</h3>
              <p className="text-gray-600">Leveraging technology to improve healthcare accessibility</p>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6 bg-gradient-to-r from-purple-600 to-blue-500 text-white">
        <div className="container mx-auto max-w-4xl text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Experience Better Healthcare?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of satisfied patients who trust TeleCareZone
          </p>
          <Button onClick={() => navigate('/')} size="lg" className="bg-white text-purple-600 hover:bg-gray-100">
            Get Started <ArrowRight className="ml-2 w-5 h-5" />
          </Button>
        </div>
      </section>
    </div>
  );
}
