# API Research: TfL vs Google Maps for Commute Times

## TfL Unified API
- **Cost**: Free (requires registration for higher limits).
- **Limits**: 50 requests per minute (default); can be increased to 500+ with an App Key/ID.
- **Coverage**: Greater London (Tube, Bus, Overground, DLR, Elizabeth Line, Trams).
- **Pros**: Zero cost, very accurate for London transit.
- **Cons**: Limited to Greater London.

## Google Maps Distance Matrix API
- **Cost**: $5.00 per 1,000 elements (Distance Matrix), $20.00 per 1,000 requests (Directions). Includes $200 monthly free credit.
- **Limits**: High, but requires billing setup and credit card.
- **Coverage**: Global.
- **Pros**: Comprehensive (includes walking/cycling), national/international.
- **Cons**: High friction for setup, potential for unexpected costs if free credit is exceeded.

## Recommendation
For the initial "London-First" version of **UK Letting Researcher**, the **TfL Unified API** is the preferred choice due to its zero-cost and high-quality data for London transit. Google Maps remains a viable fallback for future UK-wide expansion.
