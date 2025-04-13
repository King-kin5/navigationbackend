import json
import re
from backend.database.base import SessionLocal
from backend.database.models.building import Building
from backend.utils.image_utils import get_image_url

def slugify(text):
    """Convert a string to a URL-friendly slug."""
    # Replace spaces with hyphens and convert to lowercase
    slug = text.lower().replace(' ', '-')
    # Remove special characters
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Remove multiple consecutive hyphens
    slug = re.sub(r'-+', '-', slug)
    return slug

# Sample building data from your frontend
buildings_data =[
  {
    "id": "new-building",
    "slug": "new-building",
    "name": "New Building",
    "department": "School of Technology",
    "description": "A modern facility housing various technology departments and labs.",
    "facilities": ["Lecture Halls", "Computer Labs", "Research Centers", "Study Areas"],
    "coordinates": { "lat": 6.518611, "lng": 3.372723 },
    "image": "/images/buildings/new-building.jpg"
  },
  {
    "id": "etf-building",
    "slug": "etf-building",
    "name": "ETF Building",
    "department": "School of Engineering",
    "description": "The Electrical and Telecommunications Engineering facility with specialized labs and equipment.",
    "facilities": ["Electronics Lab", "Telecommunications Lab", "Workshop", "Lecture Rooms"],
    "coordinates": { "lat": 6.518834, "lng": 3.372500 },
    "image": "/images/buildings/etf-building.jpg"
  },
  {
    "id": "science-complex",
    "slug": "science-complex",
    "name": "Science Complex",
    "department": "School of Science",
    "description": "A modern complex housing the departments of Mathematics, SLT, Foodtech, Statistic, and Computer Science.",
    "facilities": ["Laboratories", "Lecture Halls", "Research Centers", "Staff Offices"],
    "coordinates": { "lat": 6.517899, "lng": 3.372577 },
    "image": "/images/buildings/science-complex.jpg"
  },
  {
    "id": "engineering-block",
    "slug": "engineering-block",
    "name": "Engineering Block",
    "department": "School of Engineering",
    "description": "Home to the various engineering departments including Civil, Mechanical, Electrical, and Computer Engineering.",
    "facilities": ["Workshops", "Design Studios", "Computer Labs", "Lecture Rooms"],
    "coordinates": { "lat": 6.517094, "lng": 3.374624 },
    "image": "/images/buildings/engineering-block.jpg"
  },
  {
    "id": "library",
    "slug": "central-library",
    "name": "Central Library",
    "department": "Library Services",
    "description": "The main library containing thousands of books, journals, and digital resources for students and staff.",
    "facilities": ["Reading Rooms", "Digital Resource Center", "Archives", "Study Carrels"],
    "coordinates": { "lat": 6.517629, "lng": 3.375300 },
    "image": ""
  },
  {
    "id": "art-design",
    "slug": "art-design-building",
    "name": "Art & Design Building",
    "department": "School of Art, Design & Printing",
    "description": "A creative hub for students studying Fine Arts, Graphic Design, and Printing Technology.",
    "facilities": ["Art Studios", "Design Labs", "Exhibition Space", "Printing Workshop"],
    "coordinates": { "lat": 6.517800, "lng": 3.373074 },
    "image": "/images/buildings/art-design-building.jpg"
  },
  {
    "id": "senate-building",
    "slug": "senate-building",
    "name": "Senate Building",
    "department": "Administration",
    "description": "The administrative headquarters housing the Rector's office, other principal officers, and administrative staff.",
    "facilities": ["Council Chamber", "Conference Rooms", "Administrative Offices", "Reception Area"],
    "coordinates": { "lat": 6.518075, "lng": 3.371708 },
    "image": ""
  },
  {
    "id": "college-hall",
    "slug": "college-hall",
    "name": "College Hall",
    "department": "Student Affairs",
    "description": "A large multipurpose hall used for academic gatherings, examinations, and other college-wide events.",
    "facilities": ["Main Hall", "Stage", "Audio System", "Exam Hall", "Meeting Rooms"],
    "coordinates": { "lat": 6.516556, "lng": 3.374922 },
    "image": ""
  },
  {
    "id": "bakassi",
    "slug": "bakassi-hostel",
    "name": "Bakassi Hostel",
    "department": "Student Affairs",
    "description": "A student residential facility providing accommodation for students with modern amenities and facilities.",
    "facilities": ["Rooms", "Common Areas", "Study Rooms", "Laundry Facilities"],
    "coordinates": { "lat": 6.519497, "lng": 3.374047 },
    "image": ""
  },
  {
    "id": "sports-complex",
    "slug": "sports-complex",
    "name": "Sports Complex",
    "department": "Sports Unit",
    "description": "A comprehensive sports facility with fields, courts, and indoor sports areas for various athletic activities.",
    "facilities": ["Football Field", "Basketball Court", "Tennis Court", "Indoor Sports Hall", "Swimming Pool"],
    "coordinates": { "lat": 6.518735, "lng": 3.374362 },
    "image": "/images/buildings/sports-complex.jpg"
  },
  {
    "id": "polymer-textile",
    "slug": "polymer-textile-building",
    "name": "Polymer and Textile Building",
    "department": "School of Engineering",
    "description": "Specialized facility for polymer science and textile engineering studies with modern laboratories.",
    "facilities": ["Textile Labs", "Polymer Labs", "Research Facilities", "Technical Workshops"],
    "coordinates": { "lat": 6.517341, "lng": 3.375633 },
    "image": "/images/buildings/polymer-textile-building.jpg"
  },
  {
    "id": "hospitality",
    "slug": "hospitality-building",
    "name": "Hospitality Building",
    "department": "School of Hospitality Management",
    "description": "Training facility for hospitality and tourism management with practical learning spaces.",
    "facilities": ["Training Kitchen", "Restaurant", "Hotel Simulation Room", "Lecture Rooms"],
    "coordinates": { "lat": 6.517239, "lng": 3.375496 },
    "image": "/images/buildings/hospitality-building.jpg"
  },
  {
    "id": "food-technology",
    "slug": "food-technology-department",
    "name": "Food Technology Department",
    "department": "Food Technology",
    "description": "The Food Technology Department specializes in food processing, preservation, quality control and product development. Features modern laboratories and pilot plant facilities.",
    "facilities": ["Food Processing Lab", "Quality Control Lab", "Product Development Kitchen", "Sensory Evaluation Room", "Food Packaging Unit"],
    "coordinates": { "lat": 6.517791, "lng": 3.375973 },
    "image": "/images/buildings/food-technology-department.jpg"
  },
  {
    "id": "zenith-bank",
    "slug": "zenith-bank",
    "name": "Zenith Bank",
    "department": "Banking Services",
    "description": "On-campus banking facility providing financial services to students and staff.",
    "facilities": ["ATM Gallery", "Banking Hall", "Customer Service"],
    "coordinates": { "lat": 6.517582, "lng": 3.374096 },
    "image": "/images/buildings/zenith-bank.jpg"
  },
  {
    "id": "pg-hostel",
    "slug": "pg-hostel",
    "name": "PG Hostel",
    "department": "Student Housing",
    "description": "Dedicated accommodation facility for postgraduate students.",
    "facilities": ["Study Rooms", "Common Areas", "Kitchenette", "Laundry Facility"],
    "coordinates": { "lat": 6.519244, "lng": 3.373658 },
    "image": ""
  },
  {
    "id": "akata-hostel",
    "slug": "akata-hostel",
    "name": "Akata Hostel",
    "department": "Student Housing",
    "description": "Student residential facility providing comfortable living spaces.",
    "facilities": ["Study Areas", "Recreation Room", "Laundry Services", "Security"],
    "coordinates": { "lat": 6.519606, "lng": 3.372915 },
    "image": ""
  }
]

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing data
        #db.query(Building).delete()
        
        # Insert new data
        for building_data in buildings_data:
            # Generate slug from name
            slug = slugify(building_data["name"])
            
            # Use predefined image URL from data
            image_url = building_data.get("image")
            
            # If no image URL provided, try to get it from existing files
            if not image_url:
                image_url = get_image_url(slug)
            
            building = Building(
                id=building_data["id"],
                slug=slug,
                name=building_data["name"],
                department=building_data["department"],
                description=building_data["description"],
                facilities=building_data["facilities"],
                coordinates=building_data["coordinates"],  # Directly store dict
                image=image_url  # Add image URL
            )
            db.add(building)
        
        db.commit()
        print(f"Successfully seeded {len(buildings_data)} buildings")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()