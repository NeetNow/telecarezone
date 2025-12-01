import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Video, Users, UserPlus, Settings } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function MainLanding() {
  const navigate = useNavigate();
  const [professionals, setProfessionals] = useState([]);

  useEffect(() => {
    fetchProfessionals();
  }, []);

  const fetchProfessionals = async () => {
    try {
      const response = await axios.get(`${API}/professionals/approved`);
      setProfessionals(response.data);
    } catch (error) {
      console.error('Error fetching professionals:', error);
    }
  };

  const getInitials = (firstName, lastName) => {
    return `${firstName?.charAt(0) || ''}${lastName?.charAt(0) || ''}`;
  };

  return (
    <div className="min-h-screen" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      {/* Navigation */}
      <nav className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
                <Video className="w-6 h-6 text-purple-600" />
              </div>
              <span className="text-2xl font-bold text-white" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                TeleCareZone
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                className="text-white hover:bg-white/20"
                onClick={() => navigate('/join-expert')}
                data-testid="nav-join-expert-btn"
              >
                Join as Expert - FREE
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-block mb-4 px-4 py-2 bg-yellow-300 text-purple-900 rounded-full font-semibold">
            🎉 Join FREE - Zero Charges for Creating Profile
          </div>
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold text-white mb-6" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Healthcare Experts
            <br />
            <span className="text-yellow-300">At Your Fingertips</span>
          </h1>
          <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
            Connect with verified healthcare professionals for video consultations from the comfort of your home
          </p>
          <Button 
            size="lg" 
            className="bg-white text-purple-600 hover:bg-gray-100 text-lg px-8 py-6 rounded-full font-semibold"
            onClick={() => document.getElementById('experts-section').scrollIntoView({ behavior: 'smooth' })}
            data-testid="hero-browse-experts-btn"
          >
            Browse Experts
          </Button>
        </div>
      </section>

      {/* Platform Features */}
      <section className="py-16 px-4 bg-white/5">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-white mb-12" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
            Why Choose TeleCareZone?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="bg-white/95 backdrop-blur-sm hover:shadow-2xl transition-all">
              <CardContent className="p-6 text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Verified Healthcare Professionals</h3>
                <p className="text-gray-600">All our doctors are verified with valid medical registrations and credentials</p>
              </CardContent>
            </Card>
            <Card className="bg-white/95 backdrop-blur-sm hover:shadow-2xl transition-all">
              <CardContent className="p-6 text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Video className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">HD Video Consultations</h3>
                <p className="text-gray-600">Secure, high-quality video calls with your healthcare provider from anywhere</p>
              </CardContent>
            </Card>
            <Card className="bg-white/95 backdrop-blur-sm hover:shadow-2xl transition-all">
              <CardContent className="p-6 text-center">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Settings className="w-8 h-8 text-purple-600" />
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-2">Easy Appointment Booking</h3>
                <p className="text-gray-600">Book appointments in minutes with our simple and intuitive booking system</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-16 px-4" id="experts-section">
        <div className="max-w-7xl mx-auto">
          <Tabs defaultValue="experts" className="w-full">
            <TabsList className="grid w-full max-w-2xl mx-auto grid-cols-4 mb-8 bg-white/20 backdrop-blur-sm p-1 rounded-xl" data-testid="main-tabs">
              <TabsTrigger value="experts" className="data-[state=active]:bg-white data-[state=active]:text-purple-600 rounded-lg" data-testid="tab-experts">
                <Users className="w-4 h-4 mr-2" />
                Our Experts
              </TabsTrigger>
              <TabsTrigger value="consultation" className="data-[state=active]:bg-white data-[state=active]:text-purple-600 rounded-lg" data-testid="tab-consultation">
                <Video className="w-4 h-4 mr-2" />
                Consultation
              </TabsTrigger>
              <TabsTrigger value="join" className="data-[state=active]:bg-white data-[state=active]:text-purple-600 rounded-lg" data-testid="tab-join">
                <UserPlus className="w-4 h-4 mr-2" />
                Join
              </TabsTrigger>
              <TabsTrigger value="customize" className="data-[state=active]:bg-white data-[state=active]:text-purple-600 rounded-lg" data-testid="tab-customize">
                <Settings className="w-4 h-4 mr-2" />
                Customize
              </TabsTrigger>
            </TabsList>

            {/* Our Experts Tab */}
            <TabsContent value="experts" className="mt-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {professionals.map((prof) => (
                  <Card key={prof.id} className="bg-white/95 backdrop-blur-sm hover:shadow-2xl transition-all duration-300 hover:-translate-y-1" data-testid={`expert-card-${prof.id}`}>
                    <CardContent className="p-6">
                      <div className="flex items-center space-x-4 mb-4">
                        <Avatar className="w-16 h-16">
                          <AvatarImage src={prof.profile_photo} />
                          <AvatarFallback className="bg-purple-100 text-purple-600 text-lg font-semibold">
                            {getInitials(prof.first_name, prof.last_name)}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <h3 className="text-lg font-bold text-gray-900">
                            Dr. {prof.first_name} {prof.last_name}
                          </h3>
                          <p className="text-sm text-gray-600">{prof.speciality}</p>
                        </div>
                      </div>
                      
                      <div className="space-y-2 mb-4 text-sm text-gray-700">
                        {prof.experience_years && (
                          <p><strong>Experience:</strong> {prof.experience_years} years</p>
                        )}
                        {prof.area_of_expertise && (
                          <p><strong>Expertise:</strong> {prof.area_of_expertise}</p>
                        )}
                        <p className="text-lg font-bold text-purple-600">₹{prof.consulting_fees}</p>
                      </div>

                      <Button 
                        className="w-full bg-purple-600 hover:bg-purple-700 text-white rounded-lg"
                        onClick={() => window.location.href = `https://${prof.subdomain}.${window.location.hostname.replace('www.', '')}`}
                        data-testid={`view-profile-btn-${prof.id}`}
                      >
                        View Profile
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>
              {professionals.length === 0 && (
                <div className="text-center py-16">
                  <p className="text-white text-xl">No experts available yet. Check back soon!</p>
                </div>
              )}
            </TabsContent>

            {/* Video Consultation Tab */}
            <TabsContent value="consultation" className="mt-8">
              <Card className="bg-white/95 backdrop-blur-sm max-w-3xl mx-auto">
                <CardContent className="p-8">
                  <h2 className="text-3xl font-bold text-gray-900 mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    How Video Consultation Works
                  </h2>
                  <div className="space-y-6">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-purple-600">1</span>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Browse Experts</h3>
                        <p className="text-gray-600">Choose from our verified healthcare professionals based on speciality and availability</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-purple-600">2</span>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Book Appointment</h3>
                        <p className="text-gray-600">Select a convenient time slot and provide your details</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-purple-600">3</span>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure Payment</h3>
                        <p className="text-gray-600">Complete payment securely through Razorpay</p>
                      </div>
                    </div>
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-purple-600">4</span>
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Join Meeting</h3>
                        <p className="text-gray-600">Receive Google Meet link via WhatsApp and email. Join at scheduled time</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Join as Expert Tab */}
            <TabsContent value="join" className="mt-8">
              <Card className="bg-white/95 backdrop-blur-sm max-w-3xl mx-auto">
                <CardContent className="p-8 text-center">
                  <UserPlus className="w-16 h-16 text-purple-600 mx-auto mb-4" />
                  <h2 className="text-3xl font-bold text-gray-900 mb-4" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    Join as Healthcare Expert
                  </h2>
                  <p className="text-lg text-gray-600 mb-8">
                    Are you a healthcare professional? Join our platform and reach thousands of patients seeking quality teleconsultation services.
                  </p>
                  <div className="space-y-4 text-left mb-8">
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                      <p className="text-gray-700">Get your personalized landing page</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                      <p className="text-gray-700">Manage appointments seamlessly</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                      <p className="text-gray-700">Automatic payment settlement (90% to you)</p>
                    </div>
                    <div className="flex items-center space-x-3">
                      <div className="w-2 h-2 bg-purple-600 rounded-full"></div>
                      <p className="text-gray-700">WhatsApp notifications for appointments</p>
                    </div>
                  </div>
                  <Button 
                    size="lg" 
                    className="bg-purple-600 hover:bg-purple-700 text-white text-lg px-8 rounded-lg"
                    onClick={() => navigate('/join-expert')}
                    data-testid="join-expert-cta-btn"
                  >
                    Apply Now
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            {/* Customize Tab */}
            <TabsContent value="customize" className="mt-8">
              <Card className="bg-white/95 backdrop-blur-sm max-w-3xl mx-auto">
                <CardContent className="p-8">
                  <Settings className="w-16 h-16 text-purple-600 mx-auto mb-4" />
                  <h2 className="text-3xl font-bold text-gray-900 mb-4 text-center" style={{ fontFamily: 'Space Grotesk, sans-serif' }}>
                    Personalized Experience
                  </h2>
                  <p className="text-lg text-gray-600 text-center mb-8">
                    Every healthcare professional gets a fully customized subdomain with their branding
                  </p>
                  <div className="bg-purple-50 p-6 rounded-xl">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">What you get:</h3>
                    <ul className="space-y-3 text-gray-700">
                      <li className="flex items-start space-x-3">
                        <span className="text-purple-600 font-bold">✓</span>
                        <span>Custom subdomain (e.g., drjohn.telecarezone.com)</span>
                      </li>
                      <li className="flex items-start space-x-3">
                        <span className="text-purple-600 font-bold">✓</span>
                        <span>Professional profile with photo, credentials, and bio</span>
                      </li>
                      <li className="flex items-start space-x-3">
                        <span className="text-purple-600 font-bold">✓</span>
                        <span>Social media integration (Instagram, YouTube, Twitter)</span>
                      </li>
                      <li className="flex items-start space-x-3">
                        <span className="text-purple-600 font-bold">✓</span>
                        <span>Patient testimonials and reviews</span>
                      </li>
                      <li className="flex items-start space-x-3">
                        <span className="text-purple-600 font-bold">✓</span>
                        <span>Appointment booking system</span>
                      </li>
                      <li className="flex items-start space-x-3">
                        <span className="text-purple-600 font-bold">✓</span>
                        <span>Integrated payment gateway</span>
                      </li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white/10 backdrop-blur-md border-t border-white/20 mt-20">
        <div className="max-w-7xl mx-auto px-4 py-8 text-center text-white">
          <p>© 2025 TeleCareZone. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}