import pytest
from rightmove_search import parse_property_data

def test_extract_agency_info_standard():
    """Test extracting agency name and phone from a standard listing."""
    mock_property = {
        'id': '12345',
        'price': {'displayPrices': [{'displayPrice': '£1,500 pcm'}]},
        'propertyTypeFullDescription': 'Flat',
        'displayAddress': '123 High St',
        'customer': {
            'brandTradingName': 'OpenRent',
            'branchDisplayName': 'OpenRent, London',
            'contactTelephone': '020 1234 5678'
        },
        'propertyUrl': '/prop/12345',
        'propertyImages': {'images': []},
        'bedrooms': 1,
        'location': {'latitude': 51.5, 'longitude': -0.1}
    }

    result = parse_property_data(mock_property)

    assert result['agency_name'] == 'OpenRent, London'
    assert result['agency_phone'] == '020 1234 5678'

def test_extract_agency_info_fallback_name():
    """Test fallback to brandTradingName if branchDisplayName is missing."""
    mock_property = {
        'id': '12345',
        'price': {'displayPrices': [{'displayPrice': '£1,500 pcm'}]},
        'customer': {
            'brandTradingName': 'Foxtons',
            # branchDisplayName missing
            'contactTelephone': '020 9876 5432'
        },
        'location': {}
    }

    result = parse_property_data(mock_property)

    assert result['agency_name'] == 'Foxtons'
    assert result['agency_phone'] == '020 9876 5432'

def test_extract_agency_info_missing():
    """Test handling of missing agency info."""
    mock_property = {
        'id': '12345',
        'price': {'displayPrices': [{'displayPrice': '£1,500 pcm'}]},
        'customer': {}, # Empty customer
        'location': {}
    }

    result = parse_property_data(mock_property)

    assert result['agency_name'] == ''
    assert result['agency_phone'] == ''
