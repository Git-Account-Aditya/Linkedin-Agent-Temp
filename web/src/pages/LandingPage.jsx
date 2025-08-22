import React from "react";
import { Link } from "react-router-dom";
import { FaRobot, FaChartLine, FaBullhorn, FaRegLightbulb, FaUserTie, FaNetworkWired } from "react-icons/fa";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-indigo-900 text-white">
      {/* Hero Section */}
      <div className="container mx-auto px-6 py-20">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="md:w-1/2 mb-10 md:mb-0">
            <span className="inline-block py-2 px-4 text-sm font-semibold bg-blue-600 rounded-full mb-6 animate-pulse">
              AI-Powered Professional Growth
            </span>
            <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-8">
              Revolutionize Your <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">LinkedIn Strategy</span>
            </h1>
            <p className="text-xl text-slate-300 mb-10 max-w-2xl">
              Unlock professional growth with our advanced AI-powered LinkedIn optimization platform that handles content creation, networking, and analytics.
            </p>
            <div className="flex flex-col sm:flex-row gap-5">
              <Link 
                to="/orchestrator" 
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg font-medium text-white hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-blue-500/20 text-center"
              >
                Get Started
              </Link>
              <Link 
                to="/analyze-profile" 
                className="px-8 py-4 bg-slate-700 rounded-lg font-medium hover:bg-slate-600 transform hover:scale-105 transition-all duration-300 text-center flex items-center justify-center"
              >
                <FaRegLightbulb className="mr-2" /> Analyze My Profile
              </Link>
            </div>
          </div>
          <div className="md:w-1/2 relative">
            <div className="relative">
              {/* Floating particles */}
              <div className="absolute -top-5 -left-5 w-3 h-3 bg-blue-500 rounded-full animate-ping"></div>
              <div className="absolute top-10 right-0 w-4 h-4 bg-purple-500 rounded-full animate-pulse"></div>
              <div className="absolute -bottom-5 -right-5 w-3 h-3 bg-blue-500 rounded-full animate-bounce"></div>
              
              <div className="bg-gradient-to-br from-blue-600/20 to-purple-600/20 p-8 rounded-2xl backdrop-blur-sm border border-slate-700 shadow-2xl">
                <div className="bg-slate-800 p-6 rounded-xl shadow-inner">
                  <div className="flex justify-between items-center mb-6">
                    <div className="text-green-400">
                      <div className="w-3 h-3 rounded-full bg-green-400 inline-block mr-2"></div>
                      <span>AI Agent Active</span>
                    </div>
                    <div className="text-blue-400 font-semibold">LinkedIn Agent v2.0.1</div>
                  </div>
                  
                  <div className="mt-4 space-y-4">
                    <div className="bg-slate-700 p-4 rounded-lg transform transition-all duration-300 hover:scale-105">
                      <div className="flex items-center mb-2">
                        <FaRobot className="text-blue-400 mr-2" />
                        <h3 className="font-bold">Content Generator</h3>
                      </div>
                      <p className="text-sm text-slate-300">AI crafting personalized posts based on your professional goals</p>
                    </div>
                    
                    <div className="bg-slate-700 p-4 rounded-lg transform transition-all duration-300 hover:scale-105">
                      <div className="flex items-center mb-2">
                        <FaNetworkWired className="text-purple-400 mr-2" />
                        <h3 className="font-bold">Network Builder</h3>
                      </div>
                      <p className="text-sm text-slate-300">Connecting you with relevant professionals in your field</p>
                    </div>
                    
                    <div className="bg-slate-700 p-4 rounded-lg transform transition-all duration-300 hover:scale-105">
                      <div className="flex items-center mb-2">
                        <FaChartLine className="text-green-400 mr-2" />
                        <h3 className="font-bold">Analytics Dashboard</h3>
                      </div>
                      <p className="text-sm text-slate-300">Tracking your growth and engagement over time</p>
                    </div>
                  </div>
                  
                  <div className="mt-6 pt-4 border-t border-slate-600">
                    <div className="text-center">
                      <div className="text-sm text-slate-400 mb-2">Optimal Performance Indicator</div>
                      <div className="w-full bg-slate-700 rounded-full h-3">
                        <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-3 rounded-full" style={{ width: '85%' }}></div>
                      </div>
                      <div className="mt-1 text-xs text-slate-400">85% Efficiency</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-slate-800/50">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Why Choose Our LinkedIn Agent?</h2>
            <p className="text-xl text-slate-300 max-w-3xl mx-auto">The ultimate solution for professionals looking to grow their LinkedIn presence</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 hover:border-blue-500 transition-all duration-300 transform hover:-translate-y-1 shadow-lg hover:shadow-blue-500/10 cursor-pointer">
              <div className="text-blue-400 mb-6 p-4 bg-blue-500/10 rounded-2xl inline-block">
                <FaUserTie className="text-3xl drop-shadow-lg" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Professional Persona</h3>
              <p className="text-slate-400 mb-6">Our AI creates content that aligns perfectly with your professional voice, position, and audience.</p>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                  <span>Profile optimization analysis</span>
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                  <span>Position-specific content generation</span>
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
                  <span>Industry trend monitoring</span>
                </li>
              </ul>
            </div>
            
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 hover:border-purple-500 transition-all duration-300 transform hover:-translate-y-1 shadow-lg hover:shadow-purple-500/10 cursor-pointer">
              <div className="text-purple-400 mb-6 p-4 bg-purple-500/10 rounded-2xl inline-block">
                <FaNetworkWired className="text-3xl drop-shadow-lg" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Smart Networking</h3>
              <p className="text-slate-400 mb-6">Automate personalized connection requests and professional engagements based on your goals.</p>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                  <span>Targeted connection suggestions</span>
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                  <span>Personalized networking strategy</span>
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-purple-400 rounded-full mr-2"></span>
                  <span>Optimal time scheduling for interactions</span>
                </li>
              </ul>
            </div>
            
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 hover:border-green-500 transition-all duration-300 transform hover:-translate-y-1 shadow-lg hover:shadow-green-500/10 cursor-pointer">
              <div className="text-green-400 mb-6 p-4 bg-green-500/10 rounded-2xl inline-block">
                <FaChartLine className="text-3xl drop-shadow-lg" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Growth Analytics</h3>
              <p className="text-slate-400 mb-6">Powerful dashboard that shows your progress across key professional metrics to refine your strategy.</p>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                  <span>Network growth tracking</span>
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                  <span>Engagement analysis</span>
                </li>
                <li className="flex items-center">
                  <span className="w-2 h-2 bg-green-400 rounded-full mr-2"></span>
                  <span>Content performance insights</span>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="mt-20 bg-gradient-to-r from-blue-900/30 via-purple-900/30 to-indigo-900/30 rounded-3xl p-12 border border-slate-700/50 shadow-xl">
            <div className="flex flex-col md:flex-row items-center justify-between">
              <div className="md:w-1/2 mb-10 md:mb-0">
                <h3 className="text-3xl font-bold mb-4">Ready to Elevate Your Professional Brand?</h3>
                <p className="text-xl text-slate-300">
                  Our LinkedIn Agents have helped professionals grow their networks 3x faster and increase post engagement by 250+%
                </p>
              </div>
              <div className="w-full md:w-1/2">
                <div className="max-w-xl mx-auto flex flex-col sm:flex-row gap-4">
                  <Link 
                    to="/signup" 
                    className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg font-medium text-white hover:from-blue-600 hover:to-purple-700 shadow-lg hover:shadow-blue-500/20 flex items-center justify-center"
                  >
                    Start Your Free Trial <span className="ml-2">🚀</span>
                  </Link>
                  <Link 
                    to="/demo" 
                    className="px-8 py-4 bg-slate-700 rounded-lg font-medium hover:bg-slate-600 flex items-center justify-center mt-4 sm:mt-0"
                  >
                    <FaBullhorn className="mr-2" /> Watch Demo
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Testimonial Section */}
      <div className="py-20 bg-slate-900">
        <div className="container mx-auto px-6">
          <h2 className="text-4xl font-bold text-center mb-16">Success Stories</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-lg">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold mr-4">JM</div>
                <div>
                  <h4 className="font-bold">Julia Martinez</h4>
                  <p className="text-slate-400">Marketing Director</p>
                </div>
              </div>
              <p className="text-slate-300 italic mb-6">"Within just three months, my network grew from 800 to 4,500 qualified connections and my content reach increased 5x. This tool transformed my professional visibility."</p>
              <div className="flex text-yellow-400">
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
              </div>
            </div>
            
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-lg">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center text-white font-bold mr-4">AD</div>
                <div>
                  <h4 className="font-bold">Alex Dawson</h4>
                  <p className="text-slate-400">Tech Entrepreneur</p>
                </div>
              </div>
              <p className="text-slate-300 italic mb-6">"The content suggestions have become a lifesaver. Not only has it helped me generate fresh ideas, but it's also taught me to approach marketing from a different and more effective perspective."</p>
              <div className="flex text-yellow-400">
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
              </div>
            </div>
            
            <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 shadow-lg">
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 rounded-full bg-green-600 flex items-center justify-center text-white font-bold mr-4">SR</div>
                <div>
                  <h4 className="font-bold">Samantha Rivers</h4>
                  <p className="text-slate-400">HR Professional</p>
                </div>
              </div>
              <p className="text-slate-300 italic mb-6">"The networking features are game-changing. It helped me connect with 83% more industry leaders in my field and significantly expand my professional circle."</p>
              <div className="flex text-yellow-400">
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
                <span>⭐</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-12 border-t border-slate-700/50">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-8 md:mb-0">
              <h3 className="text-2xl font-bold mb-2">
                LinkedIn<span className="text-blue-400">Agent</span>
              </h3>
              <p className="text-slate-400">Powerful AI that helps you grow your LinkedIn presence</p>
            </div>
            <div className="flex flex-col sm:flex-row gap-8">
              <div>
                <h4 className="font-bold mb-3">Platform</h4>
                <ul className="space-y-2 text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Integration</a></li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold mb-3">Company</h4>
                <ul className="space-y-2 text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
                </ul>
              </div>
              <div>
                <h4 className="font-bold mb-3">Legal</h4>
                <ul className="space-y-2 text-slate-400">
                  <li><a href="#" className="hover:text-white transition-colors">Privacy Policy</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Terms of Service</a></li>
                  <li><a href="#" className="hover:text-white transition-colors">Cookie Policy</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t border-slate-700/50 text-center text-slate-400">
            <p>© 2025 LinkedInAgent • All rights reserved</p>
          </div>
        </div>
      </footer>
    </div>
  );
}