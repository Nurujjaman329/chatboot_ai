# layout_tools.py

import requests
from google.genai import types

# Global variables (will be set in main_chat_app.py)
SERVICE_TOKEN = None
SHOP_ID = None


def set_api_tokens(service_token, shop_id):
    """Sets the API tokens required for tool execution."""
    global SERVICE_TOKEN, SHOP_ID
    SERVICE_TOKEN = service_token
    SHOP_ID = shop_id

# --------------------
# Tool declarations (JSON Schema for Gemini)
# --------------------

# --------------------
# Tool declarations
get_header_layout = {
    "name": "getHeaderLayout",
    "description": "Fetch layout for a section",
    "parameters": {
        "type": "object",
        "properties": {}
        
    }
}

update_header_layout = {
    "name": "updateHeaderLayout",
    "description": "Update layout blocks",
    "parameters": {
        "type": "object",
        "properties": {
            "_id": {"type": "STRING", "description": "Layout ID"},
            "layout": {"type": "STRING", "description": "Layout type, e.g., 'header'"},
            "blocks": {
                "type": "ARRAY",
                "description": "Updated blocks array",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "uuid": {"type": "STRING"},
                        "template": {"type": "STRING"},
                        "links": {
                            "type": "ARRAY",
                            "items": {
                                "type": "OBJECT",
                                "properties": {
                                    "label": {"type": "STRING"},
                                    "url": {"type": "STRING"},
                                    "subMenu": {
                                        "type": "ARRAY",
                                        "nullable": True,
                                        "items": {  
                                            "type": "OBJECT",
                                            "properties": {
                                                "label": {"type": "STRING"},
                                                "url": {"type": "STRING"},
                                                "link": {"type": "STRING", "nullable": True},
                                                "image": {"type": "STRING", "nullable": True},
                                                "icon": {"type": "STRING", "nullable": True},
                                                "subMenu": {  
                                                    "type": "ARRAY",
                                                    "nullable": True,
                                                    "items": {
                                                        "type": "OBJECT",
                                                        "properties": {
                                                            "label": {"type": "STRING", "nullable": True},
                                                            "url": {"type": "STRING", "nullable": True}
                                                        },  
                                                    }
                                                },
                                                "classes": {"type": "STRING", "nullable": True},
                                                "_id": {"type": "STRING", "nullable": True},
                                                "id": {"type": "STRING", "nullable": True}
                                            },
                                            "required": ["label", "url"]
                                        }
                                    },
                                    "classes": {"type": "STRING", "nullable": True},
                                    "_id": {"type": "STRING", "nullable": True},
                                    "id": {"type": "STRING", "nullable": True}
                                },
                                "required": ["label", "url", "subMenu"]
                            }
                        },
                        "reviews": {"type": "ARRAY", "items": {"type": "OBJECT"}, "nullable": True},
                        "products": {"type": "ARRAY", "items": {"type": "OBJECT"}, "nullable": True},
                        "brands": {"type": "ARRAY", "items": {"type": "OBJECT"}, "nullable": True},
                        "images": {"type": "ARRAY", "items": {"type": "OBJECT"}, "nullable": True},
                        "categories": {"type": "ARRAY", "items": {"type": "OBJECT"}, "nullable": True},
                        "allowFullWidth": {"type": "BOOLEAN", "nullable": True},
                        "classes": {"type": "STRING", "nullable": True},
                        "_id": {"type": "STRING", "nullable": True},
                        "id": {"type": "STRING", "nullable": True}
                    },
                    "required": ["uuid", "template", "links"]
                }
            }
        },
        "required": ["_id", "layout", "blocks"]
    }
}

get_footer_layout = {
    "name": "getFooterLayout",
    "description": "Fetch footer layout",
    "parameters": {"type": "object","properties": {}}
}

update_footer_layout = {
  "name": "updateFooterLayout",
  "description": "Update footer layout blocks",
  "parameters": {
    "type": "object",
    "properties": {
      "_id": { "type": "STRING" },
      "layout": { "type": "STRING" },
      "blocks": {
        "type": "ARRAY",
        "items": {
          "type": "OBJECT",
          "properties": {
            "uuid": { "type": "STRING" },
            "template": { "type": "STRING" },

            "cols": { "type": "NUMBER", "nullable": True },
            "rows": { "type": "NUMBER", "nullable": True },

            "label": { "type": "STRING", "nullable": True },

            "data": { "type": "STRING", "nullable": True },

            "image": {
              "type": "OBJECT",
              "nullable": True,
              "properties": {
                "src": { "type": "STRING", "nullable": True }
              }
            },

            "products": { "type": "ARRAY", "items": { "type": "STRING" }, "nullable": True },
            "brands": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },
            "categories": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },
            "reviews": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },

            "images": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },

            "links": {
              "type": "ARRAY",
              "nullable": True,
              "items": {
                "type": "OBJECT",
                "properties": {
                  "label": { "type": "STRING", "nullable": True },
                  "url": { "type": "STRING", "nullable": True },
                  "image": { "type": "STRING", "nullable": True },
                  "icon": { "type": "STRING", "nullable": True },
                  "imageSrc": { "type": "STRING", "nullable": True },
                  "thumbSrc": { "type": "STRING", "nullable": True },
                  "aspectRatio": { "type": "NUMBER", "nullable": True },
                  "_id": { "type": "STRING", "nullable": True },
                  "id": { "type": "STRING", "nullable": True }
                }
              }
            },

            "allowFullWidth": { "type": "BOOLEAN", "nullable": True },

            "_id": { "type": "STRING", "nullable": True },
            "id": { "type": "STRING", "nullable": True }
          },
          "required": ["uuid", "template"]
        }
      }
    },
    "required": ["_id", "layout", "blocks"]
  }
}



get_homepage_layout = {
  "name": "getHomepageLayout",
  "description": "Fetch layout for homepage",
  "parameters": {
    "type": "object",
    "properties": {}
  }
}


update_homepage_layout = {
  "name": "updateHomepageLayout",
  "description": "Update homepage layout blocks",
  "parameters": {
    "type": "object",
    "properties": {
      "_id": { "type": "STRING", "description": "Layout ID" },
      "layout": { "type": "STRING", "description": "Layout type, e.g., 'homepage'" },
      "blocks": {
        "type": "ARRAY",
        "description": "Updated blocks array",
        "items": {
          "type": "OBJECT",
          "properties": {
            "uuid": { "type": "STRING" },
            "template": { "type": "STRING" },

            "x": { "type": "NUMBER", "nullable": True },
            "y": { "type": "NUMBER", "nullable": True },
            "cols": { "type": "NUMBER", "nullable": True },
            "rows": { "type": "NUMBER", "nullable": True },

            "label": { "type": "STRING", "nullable": True },

            "data": { "type": "OBJECT", "nullable": True },

            "products": { "type": "ARRAY", "items": { "type": "STRING" }, "nullable": True },
            "brands": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },
            "categories": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },
            "reviews": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },

            "images": {
              "type": "ARRAY",
              "nullable": True,
              "items": {
                "type": "OBJECT",
                "properties": {
                  "url": { "type": "STRING", "nullable": True },
                  "src": { "type": "STRING", "nullable": True },
                  "image": { "type": "STRING", "nullable": True },
                  "_id": { "type": "STRING", "nullable": True },
                  "id": { "type": "STRING", "nullable": True }
                }
              }
            },

            "links": { "type": "ARRAY", "items": { "type": "OBJECT" }, "nullable": True },

            "allowFullWidth": { "type": "BOOLEAN", "nullable": True },
            "columns": { "type": "NUMBER", "nullable": True },
            "size": { "type": "NUMBER", "nullable": True },

            "classes": { "type": "STRING", "nullable": True },
            "_id": { "type": "STRING", "nullable": True },
            "id": { "type": "STRING", "nullable": True }
          },
          "required": ["uuid", "template"]
        }
      }
    },
    "required": ["_id", "layout", "blocks"]
  }
}


# --- Product Tools ---

get_products = {
    "name": "getProducts",
    "description": "Searches for products based on a query string (q). Use this before requesting details or listing products.",
    "parameters": {
        "type": "object",
        "properties": {
            "q": {
                "type": "STRING",
                "description": "The search query (e.g., 'cricket', 'shoes', 'bag')."
            }
        },
        "required": ["q"]
    }
}

getProductDetails = {
    "name": "getProductDetails",
    "description": "Fetches the full details of a single product using its unique ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "productId": {
                "type": "STRING",
                "description": "The unique ID of the product (e.g., '6912c32349da6e39c68b820b')."
            }
        },
        "required": ["productId"]
    }
}

createProduct = {
    "name": "createProduct",
    "description": "Creates a new product. Requires name, slug, SKU, and listPrice.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": { "type": "STRING" },
            "slug": { "type": "STRING" },
            "sku": { "type": "STRING" },
            "listPrice": { "type": "NUMBER" }
        },
        "required": ["name", "slug", "sku", "listPrice"]
    }
}

updateProduct = {
    "name": "updateProduct",
    "description": "Updates one or more fields of an existing product using its unique ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "productId": {
                "type": "STRING",
                "description": "The unique ID of the product to update."
            },
            "name": { "type": "STRING", "nullable": True },
            "listPrice": { "type": "NUMBER", "nullable": True }
            # Add other fields as needed for updates
        },
        "required": ["productId"]
    }
}

# Category Tools

getCategories = {
    "name": "getCategories",
    "description": "Searches for categories based on a query string (q). Use this before requesting details or listing categories.",
    "parameters": {
        "type": "object",
        "properties": {
            "q": {
                "type": "STRING",
                "description": "The search query (e.g., 'sunglass', 'men', 'electronics')."
            }
        },
        "required": ["q"]
    }
}

getCategoryDetails = {
    "name": "getCategoryDetails",
    "description": "Fetches the full details of a single category using its unique ID.",
    "parameters": {
        "type": "object",
        "properties": {
            "categoryId": {
                "type": "STRING",
                "description": "The unique ID of the category (e.g., '6912c3b449da6e39c68bbef6')."
            }
        },
        "required": ["categoryId"]
    }
}

createCategory = {
    "name": "createCategory",
    "description": "Creates a new category. Requires name and slug.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": { "type": "STRING" },
            "slug": { "type": "STRING" }
            # visibility can default to 'public' as per your example
        },
        "required": ["name", "slug"]
    }
}

# pages create

getPages = {
    "name": "getPages",
    "description": "Searches for static content pages by query. Use this tool when the user asks to find, list, or search for existing pages (e.g., 'Find the about us page', 'Show all pages').",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "q": {
                "type": "string",
                "description": "The search query or keyword to filter pages by title or content."
            }
        },
        "required": ["q"],
    }
}

getPageDetails = {
    "name": "getPageDetails",
    "description": "Retrieves the full details and content for a specific static page using its ID. Use this when the user asks for the full content of a known page.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "pageId": {
                "type": "string",
                "description": "The unique identifier (ID) of the page whose details are required."
            }
        },
        "required": ["pageId"],
    }
}

createPage = {
    "name": "createPage",
    "description": "Creates a new static content page. Requires a title and a slug to uniquely identify the page.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "title": {
                "type": "string",
                "description": "The display title of the new page (e.g., 'About Us')."
            },
            "slug": {
                "type": "string",
                "description": "The URL slug for the page (e.g., 'about-us'). Must be unique and in kebab-case."
            }
        },
        "required": ["title", "slug"],
    }
}


# template tool 

getTemplates = {
    "name": "getTemplates",
    "description": "Searches or lists all available website templates that can be applied to the shop. Use this when the user asks to see or find available templates.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "q": {
                "type": "string",
                "description": "The search query or keyword to filter templates by name or tag (e.g., 'fashion', 'book')."
            }
        },
        "required": [],
    }
}

setTemplate = {
    "name": "setTemplate",
    "description": "Applies a specific template to the current shop using its ID. WARNING: Applying a new template will overwrite the shop's existing Header, Footer, and Homepage layouts.",
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "id": {
                "type": "string",
                "description": "The unique identifier (ID) of the template to be applied."
            }
        },
        "required": ["id"],
    }
}




# Combine all tool declarations
ALL_TOOLS = types.Tool(
    function_declarations=[
        get_header_layout, update_header_layout,
        get_homepage_layout, update_homepage_layout,
        get_footer_layout, update_footer_layout,

        get_products, getProductDetails, createProduct, updateProduct,

        getCategories, getCategoryDetails, createCategory,

        getPages, getPageDetails, createPage,

        getTemplates, setTemplate,
    ]
)

# --------------------
# Tool Execution Logic
# --------------------

def execute_tool(name, args):
    """
    Executes the specified API tool call based on the name.
    """
    if SERVICE_TOKEN is None or SHOP_ID is None:
        return {"error": "API tokens not initialized. Cannot execute tool."}

    headers = {
        "x-edokan-service-token": SERVICE_TOKEN,
        "x-edokan-shop-id": SHOP_ID,
        "Content-Type": "application/json",
    }
    
    BASE_URL = "https://api.edokan.co/ai/mcpx"

    # Define URL Map for Layouts for clear separation
    LAYOUT_URL_MAP = {
        "header": f"{BASE_URL}/layouts/header",
        "footer": f"{BASE_URL}/layouts/footer",
        "homepage": f"{BASE_URL}/layouts/homepage",
    }

    try:
        # --- TEMPLATE TOOLS EXECUTION (NEW) ---
        if name == "getTemplates":
            # Search templates: GET /templates?q=query
            query_params = {"q": args.get("q", "")}
            # Endpoint is /templates
            return requests.get(f"{BASE_URL}/templates", headers=headers, params=query_params, timeout=10).json()
        
        elif name == "setTemplate":
            # Apply template: POST /templates/set
            template_id = args.get("id")
            if not template_id:
                return {"error": "Template ID is required for setTemplate."}
            
            # Request body structure: { "id": "..." }
            payload = {"id": template_id}
            # Endpoint is /templates/set
            return requests.post(f"{BASE_URL}/templates/set", headers=headers, json=payload, timeout=10).json()

        # --- PAGE TOOLS EXECUTION (Existing) ---
        elif name == "getPages":
            # Search pages: GET /pages?q=query
            query_params = {"q": args.get("q", "")}
            return requests.get(f"{BASE_URL}/pages", headers=headers, params=query_params, timeout=10).json()
        
        elif name == "getPageDetails":
            # Get page details: GET /pages/{pageId}
            page_id = args.get("pageId")
            if not page_id:
                return {"error": "Page ID is required for getPageDetails."}
            return requests.get(f"{BASE_URL}/pages/{page_id}", headers=headers, timeout=10).json()

        elif name == "createPage":
            # Create page: POST /pages
            payload = {k: v for k, v in args.items() if v is not None}
            # Ensure required fields for creation are present
            if not payload.get('title') or not payload.get('slug'):
                return {"error": "Title and slug are required to create a page."}
            return requests.post(f"{BASE_URL}/pages", headers=headers, json=payload, timeout=10).json()

        # --- CATEGORY TOOLS EXECUTION (Existing) ---
        elif name == "getCategories":
            # Search categories: GET /categories?q=query
            query_params = {"q": args.get("q", "")}
            return requests.get(f"{BASE_URL}/categories", headers=headers, params=query_params, timeout=10).json()
        
        elif name == "getCategoryDetails":
            # Get category details: GET /categories/{categoryId}
            category_id = args.get("categoryId")
            if not category_id:
                return {"error": "Category ID is required for getCategoryDetails."}
            return requests.get(f"{BASE_URL}/categories/{category_id}", headers=headers, timeout=10).json()

        elif name == "createCategory":
            # Create category: POST /categories
            payload = {k: v for k, v in args.items() if v is not None}
            return requests.post(f"{BASE_URL}/categories", headers=headers, json=payload, timeout=10).json()
            
        # --- PRODUCT TOOLS EXECUTION (Existing) ---
        elif name == "getProducts":
            # Search products: GET /products?q=query
            query_params = {"q": args.get("q", "")}
            return requests.get(f"{BASE_URL}/products", headers=headers, params=query_params, timeout=10).json()
        
        elif name == "getProductDetails":
            # Get product details: GET /products/{productId}
            product_id = args.get("productId")
            if not product_id:
                return {"error": "Product ID is required for getProductDetails."}
            return requests.get(f"{BASE_URL}/products/{product_id}", headers=headers, timeout=10).json()

        elif name == "createProduct":
            # Create product: POST /products
            payload = {k: v for k, v in args.items() if v is not None}
            return requests.post(f"{BASE_URL}/products", headers=headers, json=payload, timeout=10).json()

        elif name == "updateProduct":
            # Update product: PUT /products/{productId}
            product_id = args.pop("productId", None)
            if not product_id:
                return {"error": "Product ID is required for updateProduct."}
            
            # The payload contains all remaining fields (e.g., name, listPrice)
            payload = {k: v for k, v in args.items() if v is not None}
            return requests.put(f"{BASE_URL}/products/{product_id}", headers=headers, json=payload, timeout=10).json()


        # --- LAYOUT TOOLS EXECUTION (Original Logic) ---

        elif name.startswith("get") and name.endswith("Layout"):
            layout_type = name.replace("get", "").lower().replace("layout", "")
            url = LAYOUT_URL_MAP.get(layout_type)
            if url:
                return requests.get(url, headers=headers, timeout=10).json()
        
        elif name.startswith("update") and name.endswith("Layout"):
            layout_type = name.replace("update", "").lower().replace("layout", "")
            url = LAYOUT_URL_MAP.get(layout_type)
            if url:
                # Layout updates send the whole modified JSON object as the body
                return requests.put(url, headers=headers, json=args, timeout=10).json()

        return {"error": f"Unknown or unhandled tool: {name}"}

    except requests.RequestException as e:
        return {"error": f"API Request Failed for {name}: {e}"}