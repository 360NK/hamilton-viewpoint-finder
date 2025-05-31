# Hamilton Viewspot Finder - Project Design Document

**Version:** 1.0  
**Last Updated:** January 2025  
**Project Type:** Advanced Spatial Analysis Platform for Recreational Planning

## Project Vision

**Goal:** Interactive web platform for discovering optimal recreational viewpoints along Hamilton's Niagara Escarpment using advanced viewshed analysis.

**Target Use Case:** Tourism and recreation planning - "Find the perfect chill spots with epic views along Hamilton's escarpment"

**Core Value Proposition:** Interactive tool to discover scenic viewpoints optimized for recreation, with practical info about access, privacy, and conditions.

---

## Current Project Status

### ✅ COMPLETED MILESTONES

**Data Acquisition & Processing:**

- [x] Located HRDEM 2m DSM COG tiles (8_1, 8_2) for Hamilton area
- [x] Downloaded Niagara Escarpment Plan boundary shapefile
- [x] Downloaded Hamilton municipal boundary shapefile
- [x] **Successfully intersected boundaries to create precise study area**
- [x] Confirmed 2m DSM covers Hamilton escarpment completely
- [x] Set up conda environment with spatial libraries (gdal, rasterio, geopandas)

**Technical Decisions Made:**

- [x] **2m DSM selected** over 1m (balance of detail vs. processing efficiency)
- [x] **DSM chosen over DTM** (realistic visibility including buildings/trees)
- [x] **Cloud COG workflow** instead of local 77GB downloads
- [x] **Official boundary intersection** for scientifically-defined study area
- [x] **Recreation-focused use case** (finding chill spots with good views)

### 🔄 CURRENT PHASE: Data Validation & Clipping

**Immediate Next Steps:**

1. Validate COG access to HRDEM tiles
2. Clip DEM data using intersected boundary geometry
3. Prepare working dataset for viewshed algorithm development

---

## Technical Architecture Design

### Data Stack

```
Data Sources:
├── Elevation: HRDEM 2m DSM (Cloud COGs)
│   ├── Tile 8_1: https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_1-mosaic-2m-dsm.tif
│   └── Tile 8_2: https://datacube-prod-data-public.s3.amazonaws.com/store/elevation/hrdem/hrdem-mosaic-2m/8_2-mosaic-2m-dsm.tif
├── Boundaries: Official Government Shapefiles
│   ├── Niagara Escarpment Plan Area (Ontario GeoHub)
│   ├── Hamilton Municipal Boundary (Hamilton Open Data)
│   └── **Intersection Result: Precise Hamilton Escarpment Study Area** ✅
├── Validation: Ground Truth Photography (Planned)
└── Environmental: Weather APIs (Future)
```

### Application Architecture

```
Backend (Python):
├── Spatial Processing Engine
│   ├── Core Viewshed Algorithm (Line-of-sight calculation)
│   ├── Recreational Scoring System (Privacy, access, scenic quality)
│   ├── Performance Optimization (Spatial indexing, caching)
│   └── Data Pipeline (COG processing, boundary operations)
├── API Layer (FastAPI)
│   ├── Viewshed calculation endpoints
│   ├── Real-time analysis triggers
│   └── Results export capabilities
└── Database (PostGIS)
    ├── Processed DEM storage
    ├── Analysis results caching
    └── Validation data management

Frontend (Future):
├── Interactive Mapping (React + Leaflet)
├── Real-time Viewshed Visualization
├── Practical Information Display
└── Export/Sharing Capabilities
```

---

## Key Technical Decisions & Rationale

### 1. Data Resolution: 2m DSM

**Decision:** Use 2m resolution Digital Surface Model
**Rationale:**

- **Sufficient Detail:** Captures buildings, forest canopy, terrain features adequately
- **Processing Efficiency:** 4x faster than 1m, manageable file sizes
- **Realistic Analysis:** DSM includes trees/buildings for authentic viewshed results
- **Scalability:** Can handle regional analysis without performance issues

### 2. Study Area Definition: Boundary Intersection

**Decision:** Intersect official Niagara Escarpment + Hamilton boundaries
**Rationale:**

- **Scientific Accuracy:** Uses authoritative, legally-defined boundaries
- **Precise Coverage:** Captures complete escarpment within Hamilton
- **Professional Methodology:** Demonstrates proper spatial analysis workflow
- **Defensible Results:** Based on official government data sources

### 3. Cloud-Native Processing: COG Workflow

**Decision:** Access HRDEM via Cloud Optimized GeoTIFFs, clip remotely
**Rationale:**

- **Efficiency:** Download only needed area (MB vs. 77GB per tile)
- **Modern Approach:** Industry-standard cloud geospatial processing
- **Storage Savings:** Minimal local storage requirements
- **Always Current:** Access latest government data directly

### 4. Recreation-Focused Use Case

**Decision:** Optimize for finding "chill spots with good views"
**Rationale:**

- **Personal Motivation:** Genuine user need drives better development
- **Validation Advantage:** Can personally test all recommendations
- **Unique Positioning:** Different from typical GIS portfolio projects
- **Practical Value:** Creates actually useful recreational tool

---

## Enhanced Viewshed Algorithm Design

### Core Technical Components

**1. Basic Viewshed Calculation**

```python
# Line-of-sight algorithm accounting for:
- Observer height (1.7m standard person height)
- Earth curvature (for distant views >10km)
- Terrain occlusion (hills, valleys)
- Surface features (buildings, trees via DSM)
```

**2. Recreational Scoring System**

```python
recreational_score = weighted_average({
    'scenic_quality': 40%,      # Lake visibility, skyline views, natural areas
    'privacy_level': 30%,       # Seclusion, distance from crowds
    'accessibility': 20%,       # Walking distance, terrain difficulty
    'weather_protection': 10%   # Wind shelter, overhead cover
})
```

**3. Advanced Features**

- **Reverse Viewshed:** Who can see you? (Privacy analysis)
- **Seasonal Adjustments:** Winter vs. summer visibility through vegetation
- **Time-of-Day Optimization:** Best lighting conditions
- **Multi-criteria Analysis:** Combine visibility with practical factors

---

## Validation Strategy

### Ground Truth Photography Plan

**Systematic Field Validation:**

- **Phase 1:** Test 5 known viewpoints (Dundurn Castle, Devil's Punchbowl, etc.)
- **Phase 2:** Validate 10-15 algorithm-predicted spots
- **Phase 3:** User testing with local hikers/photographers

**Documentation Protocol:**

- Panoramic photos from each viewpoint
- GPS coordinates and elevation readings
- Access route documentation
- Privacy/crowding assessment
- Weather/visibility conditions

**Success Metrics:**

- 85%+ accuracy in landmark visibility prediction
- Strong correlation (r>0.7) between predicted and actual scenic scores
- User satisfaction >75% for algorithm recommendations

---

## Implementation Roadmap

### Week 1: Data Foundation (Current)

- [x] **Boundary intersection completed**
- [ ] Validate COG access and coverage
- [ ] Clip HRDEM to study area using intersection boundary
- [ ] Prepare clean working dataset

### Week 2: Core Algorithm Development

- [ ] Implement basic line-of-sight viewshed calculation
- [ ] Test accuracy with known viewpoints (Dundurn, Devil's Punchbowl)
- [ ] Optimize for 2m DSM processing
- [ ] Performance benchmarking (<10 second calculation target)

### Week 3: Recreational Scoring Implementation

- [ ] Develop scenic quality assessment algorithms
- [ ] Implement privacy/seclusion analysis
- [ ] Add accessibility scoring (slope, distance analysis)
- [ ] Integrate multi-criteria decision framework

### Week 4: Validation & Testing

- [ ] Systematic field validation campaign
- [ ] Photo documentation of predicted vs. actual views
- [ ] Algorithm accuracy assessment and refinement
- [ ] Performance optimization

### Week 5-6: Web Interface Development

- [ ] Interactive mapping interface (React + Leaflet)
- [ ] Real-time viewshed calculation API
- [ ] Results visualization and export features
- [ ] Mobile-responsive design

### Week 7-8: Advanced Features & Deployment

- [ ] Environmental data integration (weather, seasonal factors)
- [ ] Advanced visualization (3D viewsheds, time-series)
- [ ] Production deployment and documentation
- [ ] Portfolio presentation preparation

---

## Risk Management & Contingencies

### Technical Risks

**COG Access Issues:** Backup plan with local DEM processing if cloud access fails
**Performance Bottlenecks:** Spatial indexing and caching strategies prepared
**Algorithm Complexity:** Start with basic viewshed, add sophistication incrementally

### Timeline Risks

**Scope Management:** Core functionality prioritized, advanced features as stretch goals
**Weather Dependency:** Indoor validation alternatives for field work
**Learning Curve:** Buffer time allocated for new technology mastery

### Success Criteria

**Technical:** Interactive viewshed analysis with <10 second response time
**Practical:** Accurately identifies 8/10 high-quality viewpoints through validation
**Portfolio:** Professional demonstration ready for employer presentation

---

## Current File Structure

```
hamilton-viewspot-finder/
├── backend/
│   ├── app/
│   ├── scripts/
│   ├── data/
│   │   ├── raw/
│   │   │   ├── niagara_escarpment_boundary.shp ✅
│   │   │   └── hamilton_boundary.shp ✅
│   │   └── processed/
│   │       └── hamilton_escarpment_intersection.shp ✅
│   └── tests/
├── docs/
│   ├── learning_log.md
│   ├── technical_decisions.md
│   ├── validation_plan.md
│   └── this_design_document.md
└── README.md
```

---

## Immediate Action Items

### Next Session Goals:

1. **COG Validation Script:** Verify access to HRDEM tiles and examine coverage
2. **DEM Clipping Pipeline:** Use intersection boundary to extract working dataset
3. **Algorithm Planning:** Design basic viewshed implementation approach
4. **Validation Preparation:** Plan first field testing trip

### Questions to Resolve:

- Exact coordinate system handling between boundaries and DEM
- Optimal processing approach for 2m DSM data
- Performance targets for interactive viewshed calculation
- Ground truth validation schedule and methodology

---

## Version Control & Updates

**Document Updates:** This design document will be updated after each major milestone
**Change Log:** All technical decisions and scope modifications documented
**Review Schedule:** Weekly assessment of progress against timeline and goals

**Next Update Trigger:** Completion of COG validation and DEM clipping phase
