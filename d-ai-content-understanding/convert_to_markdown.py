import json
import argparse
from pathlib import Path

def format_value(value):
    """Format a value for markdown display."""
    if value is None or value == "":
        return "NA"
    if isinstance(value, list) and len(value) == 0:
        return "NA"
    if isinstance(value, dict) and len(value) == 0:
        return "NA"
    return value

def process_scenes(scenes_array):
    """Convert scenes array to markdown table."""
    if not scenes_array:
        return "NA\n"
    
    table = "| Description | StartTimestamp | EndTimestamp | Location | EraEstimatedYear | EraReasoning | Brands | Celebrities | ShotType | ColorScheme | IsSignatureMoment |\n"
    table += "|-------------|----------------|--------------|----------|------------------|--------------|--------|-------------|----------|-------------|-------------------|\n"
    
    for scene in scenes_array:
        if isinstance(scene, dict) and scene.get("type") == "object":
            obj = scene.get("valueObject", {})
            desc = obj.get("Description", {}).get("valueString", "NA")
            start_ts = obj.get("StartTimestamp", {}).get("valueString", "NA")
            end_ts = obj.get("EndTimestamp", {}).get("valueString", "NA")
            location = obj.get("Location", {}).get("valueString", "NA")
            era_year = obj.get("EraEstimatedYear", {}).get("valueString", "NA")
            era_reasoning = obj.get("EraReasoning", {}).get("valueString", "NA")
            brands = obj.get("Brands", {}).get("valueString", "NA")
            celebrities = obj.get("Celebrities", {}).get("valueString", "NA")
            shot_type = obj.get("ShotType", {}).get("valueString", "NA")
            color_scheme = obj.get("ColorScheme", {}).get("valueString", "NA")
            is_signature = obj.get("IsSignatureMoment", {}).get("valueBoolean", "NA")
            
            # Escape pipe characters
            for val in [desc, location, era_reasoning, brands, celebrities, shot_type, color_scheme]:
                if val != "NA" and isinstance(val, str):
                    val = val.replace("|", "\\|")
            
            # Handle empty strings
            if desc == "": desc = "NA"
            if start_ts == "": start_ts = "NA"
            if end_ts == "": end_ts = "NA"
            if location == "": location = "NA"
            if era_year == "": era_year = "NA"
            if era_reasoning == "": era_reasoning = "NA"
            if brands == "": brands = "NA"
            if celebrities == "": celebrities = "NA"
            if shot_type == "": shot_type = "NA"
            if color_scheme == "": color_scheme = "NA"
            
            table += f"| {desc} | {start_ts} | {end_ts} | {location} | {era_year} | {era_reasoning} | {brands} | {celebrities} | {shot_type} | {color_scheme} | {is_signature} |\n"
    
    return table

def process_transcript_phrases(phrases):
    """Convert transcript phrases to markdown table."""
    if not phrases:
        return "NA\n"
    
    table = "| Speaker | Start Time (ms) | End Time (ms) | Text | Confidence | Locale |\n"
    table += "|---------|-----------------|---------------|------|------------|--------|\n"
    
    for phrase in phrases:
        speaker = phrase.get("speaker", "NA")
        start = phrase.get("startTimeMs", "NA")
        end = phrase.get("endTimeMs", "NA")
        text = phrase.get("text", "NA")
        if text != "NA":
            text = text.replace("|", "\\|")
        confidence = phrase.get("confidence", "NA")
        locale = phrase.get("locale", "NA")
        
        table += f"| {speaker} | {start} | {end} | {text} | {confidence} | {locale} |\n"
    
    return table

def process_segment(segment_data, segment_num):
    """Process a single segment."""
    if segment_data.get("type") != "object":
        return ""
    
    value_obj = segment_data.get("valueObject", {})
    
    output = f"\n**Segment {segment_num}**\n\n"
    
    # Process all fields except Scenes
    for key, field in value_obj.items():
        if key == "Scenes":
            continue  # Handle scenes separately
        
        field_type = field.get("type")
        
        if field_type == "string":
            value = format_value(field.get("valueString"))
            output += f"- **{key}**: {value}\n"
        elif field_type == "boolean":
            value = field.get("valueBoolean")
            output += f"- **{key}**: {value}\n"
        elif field_type == "array":
            array_val = field.get("valueArray", [])
            if len(array_val) == 0:
                output += f"- **{key}**: NA\n"
            else:
                output += f"- **{key}**:\n"
                for item in array_val:
                    if isinstance(item, str):
                        output += f"  - {item}\n"
                    elif isinstance(item, dict):
                        # Parse nested objects with type/valueString structure
                        if item.get("type") == "string" and "valueString" in item:
                            output += f"  - {item['valueString']}\n"
                        else:
                            output += f"  - {json.dumps(item)}\n"
    
    # Handle Scenes as a table
    if "Scenes" in value_obj:
        output += f"\n**Scenes**\n\n"
        scenes_data = value_obj["Scenes"].get("valueArray", [])
        output += process_scenes(scenes_data)
    
    return output

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Convert video analysis JSON to markdown')
    parser.add_argument('input_file', nargs='?', default='results.json', 
                        help='Input JSON file (default: results.json)')
    args = parser.parse_args()
    
    # Generate output filename with .md extension
    input_path = Path(args.input_file)
    output_file = input_path.with_suffix('.md')
    
    # Load JSON
    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Start markdown output
    md_output = "# Video Analysis Results\n\n"
    
    # Top-level fields
    md_output += f"## General Information\n\n"
    md_output += f"- **id**: {format_value(data.get('id'))}\n"
    md_output += f"- **status**: {format_value(data.get('status'))}\n\n"
    
    # Usage section
    if "usage" in data:
        md_output += f"## Usage\n\n"
        usage = data["usage"]
        md_output += f"- **videoHours**: {format_value(usage.get('videoHours'))}\n"
        md_output += f"- **contextualizationTokens**: {format_value(usage.get('contextualizationTokens'))}\n"
        
        if "tokens" in usage:
            md_output += f"- **tokens**:\n"
            for key, val in usage["tokens"].items():
                md_output += f"  - **{key}**: {format_value(val)}\n"
        md_output += "\n"
    
    # Warnings section
    if "result" in data and "warnings" in data["result"]:
        md_output += f"## Warnings\n\n"
        warnings = data["result"]["warnings"]
        if warnings:
            for warning in warnings:
                md_output += f"- **Code**: {warning.get('code', 'NA')}\n"
                md_output += f"  - **Message**: {warning.get('message', 'NA')}\n"
                md_output += f"  - **Target**: {warning.get('target', 'NA')}\n"
        else:
            md_output += "NA\n"
        md_output += "\n"
    
    # Result section
    if "result" in data:
        result = data["result"]
        md_output += f"## Result\n\n"
        md_output += f"- **analyzerId**: {format_value(result.get('analyzerId'))}\n"
        md_output += f"- **apiVersion**: {format_value(result.get('apiVersion'))}\n"
        md_output += f"- **createdAt**: {format_value(result.get('createdAt'))}\n\n"
    
    # Contents section
    if "result" in data and "contents" in data["result"]:
        contents = data["result"]["contents"]
        
        for idx, content in enumerate(contents, 1):
            md_output += f"## Content {idx}\n\n"
            
            # Basic content properties
            md_output += f"- **kind**: {format_value(content.get('kind'))}\n"
            md_output += f"- **startTimeMs**: {format_value(content.get('startTimeMs'))}\n"
            md_output += f"- **endTimeMs**: {format_value(content.get('endTimeMs'))}\n"
            md_output += f"- **width**: {format_value(content.get('width'))}\n"
            md_output += f"- **height**: {format_value(content.get('height'))}\n"
            md_output += f"- **mimeType**: {format_value(content.get('mimeType'))}\n\n"
            
            # Markdown field (with 4 backticks)
            if "markdown" in content:
                md_output += f"**Markdown**:\n\n````markdown\n{content['markdown']}\n````\n\n"
            
            # KeyFrameTimesMs
            if "KeyFrameTimesMs" in content:
                md_output += f"**KeyFrameTimesMs**:\n\n"
                key_frames = content["KeyFrameTimesMs"]
                if key_frames:
                    for kf in key_frames:
                        md_output += f"- {kf}\n"
                else:
                    md_output += "NA\n"
                md_output += "\n"
            
            # cameraShotTimesMs
            if "cameraShotTimesMs" in content:
                md_output += f"**cameraShotTimesMs**:\n\n"
                camera_shots = content["cameraShotTimesMs"]
                if camera_shots:
                    for cs in camera_shots:
                        md_output += f"- {cs}\n"
                else:
                    md_output += "NA\n"
                md_output += "\n"
            
            # transcriptPhrases
            if "transcriptPhrases" in content:
                md_output += f"**transcriptPhrases**:\n\n"
                md_output += process_transcript_phrases(content["transcriptPhrases"])
                md_output += "\n"
            
            # Fields section (continuing as part of Content)
            if "fields" in content:
                fields = content["fields"]
                
                # Description field
                if "Description" in fields:
                    desc = fields["Description"].get("valueString", "NA")
                    md_output += f"**Description**: {desc}\n\n"
                
                # Segments
                if "Segments" in fields:
                    md_output += f"**Segments**:\n"
                    segments = fields["Segments"].get("valueArray", [])
                    
                    if segments:
                        for seg_idx, segment in enumerate(segments, 1):
                            md_output += process_segment(segment, seg_idx)
                    else:
                        md_output += "\nNA\n"
                    md_output += "\n"
    
    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_output)
    
    print(f"Markdown file '{output_file}' created successfully!")

if __name__ == "__main__":
    main()
