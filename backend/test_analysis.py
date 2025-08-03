#!/usr/bin/env python3
"""
Test script for Phase 3 AI Analysis Engine
"""
import asyncio
import json
import httpx
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_analysis_api():
    """Test the complete analysis API flow."""
    
    print("🧪 Testing Website Design Scorer - Phase 3 AI Analysis")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        
        # 1. Test health endpoints
        print("\n1️⃣ Testing Health Endpoints...")
        try:
            # Basic health
            response = await client.get(f"{BASE_URL}/api/v1/health")
            print(f"✅ Basic Health: {response.status_code}")
            
            # Analysis health
            response = await client.get(f"{BASE_URL}/api/v1/analysis/health")
            health_data = response.json()
            print(f"✅ Analysis Health: {response.status_code}")
            print(f"   Ollama Connection: {'✅' if health_data.get('ollama_connection') else '❌'}")
            print(f"   Cloudinary Connection: {'✅' if health_data.get('cloudinary_connection') else '❌'}")
            
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # 2. Start analysis
        print("\n2️⃣ Starting Website Analysis...")
        test_url = "https://example.com"
        
        try:
            analysis_request = {
                "url": test_url,
                "include_mobile": True,
                "include_llm_analysis": True
            }
            
            response = await client.post(
                f"{BASE_URL}/api/v1/analysis/analyze",
                json=analysis_request
            )
            
            if response.status_code != 200:
                print(f"❌ Analysis request failed: {response.status_code}")
                print(response.text)
                return
                
            analysis_data = response.json()
            analysis_id = analysis_data["analysis_id"]
            print(f"✅ Analysis started: {analysis_id}")
            print(f"   Status: {analysis_data['status']}")
            
        except Exception as e:
            print(f"❌ Analysis request failed: {e}")
            return
        
        # 3. Poll for completion
        print("\n3️⃣ Polling for Analysis Completion...")
        max_attempts = 40  # 2 minutes max
        attempt = 0
        
        while attempt < max_attempts:
            try:
                response = await client.get(f"{BASE_URL}/api/v1/analysis/status/{analysis_id}")
                status_data = response.json()
                
                status = status_data["status"]
                progress = status_data.get("progress", {})
                
                print(f"   [{attempt+1:2d}/{max_attempts}] Status: {status} - {progress.get('stage', 'N/A')} ({progress.get('percentage', 0)}%)")
                
                if status == "completed":
                    print("✅ Analysis completed!")
                    break
                elif status == "error":
                    print(f"❌ Analysis failed: {status_data.get('error', 'Unknown error')}")
                    return
                
                await asyncio.sleep(3)
                attempt += 1
                
            except Exception as e:
                print(f"❌ Status check failed: {e}")
                break
        
        if attempt >= max_attempts:
            print("❌ Analysis timed out")
            return
        
        # 4. Get final results
        print("\n4️⃣ Retrieving Analysis Results...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/analysis/result/{analysis_id}")
            
            if response.status_code != 200:
                print(f"❌ Failed to get results: {response.status_code}")
                return
                
            result_data = response.json()
            
            print("✅ Analysis Results:")
            print(f"   Overall Score: {result_data.get('overall_score', 0)}/100")
            print(f"   Analysis Duration: {result_data.get('analysis_duration', 0):.2f}s")
            
            # Score breakdown
            scores = result_data.get('scores_breakdown', {})
            print("\n📊 Score Breakdown:")
            for category, score in scores.items():
                print(f"   {category.title()}: {score}/100")
            
            # LLM Analysis
            llm_analysis = result_data.get('llm_analysis', {})
            if llm_analysis.get('content'):
                print(f"\n🧠 LLM Analysis Preview:")
                content = llm_analysis['content'][:200]
                print(f"   {content}{'...' if len(llm_analysis['content']) > 200 else ''}")
            elif llm_analysis.get('error'):
                print(f"\n⚠️  LLM Analysis Error: {llm_analysis['error']}")
            
            # Screenshots
            screenshots = result_data.get('screenshots', {})
            if screenshots.get('desktop'):
                print(f"\n📸 Desktop Screenshot: {screenshots['desktop'].get('local_path', 'N/A')}")
            if screenshots.get('mobile'):
                print(f"📱 Mobile Screenshot: {screenshots['mobile'].get('local_path', 'N/A')}")
                
        except Exception as e:
            print(f"❌ Failed to retrieve results: {e}")
            return
        
        # 5. Test listing analyses
        print("\n5️⃣ Testing Analysis List...")
        try:
            response = await client.get(f"{BASE_URL}/api/v1/analysis/list")
            list_data = response.json()
            print(f"✅ Found {list_data.get('total', 0)} analyses")
            
        except Exception as e:
            print(f"❌ List analyses failed: {e}")
    
    print("\n🎉 Phase 3 AI Analysis Engine Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_analysis_api())
