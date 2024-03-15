//
//  RecipesView.swift
//  project
//
//  Created by Drew S on 3/6/24.
//

import SwiftUI

struct Recipe: Codable {
    let name: String
    let url: String
}

struct RecipesView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)
    
    @State private var recipes: [Recipe] = []

    var body: some View {
        VStack{
            VStack
            {
                HStack{
                    Text("Recipes")
                        .foregroundColor(textGrey)
                        .font(.system(size:40))
                        .padding(.horizontal, 30)
                    Spacer()
                }
                
            }.background(Color.black)
            Spacer()
            
            ScrollView {
                VStack(spacing: 20) {
                    ForEach(recipes, id: \.name) { recipe in PreviewBox(color:boxGrey, recipe:recipe)
                    }
                }
                .padding()
            }

        }.background(Color.black)
            .onAppear{recipes = loadRecipes()}
    }
    
    
    
    func loadJSONData(from filename: String) -> [String: Any]? {
        if let url = Bundle.main.url(forResource: filename, withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                // convert json data to any object
                let jsonObject = try JSONSerialization.jsonObject(with: data, options: [])
                
                //print("json object:")
                //print(jsonObject)
                
                // convert any object to [String: Any] dictionary
                guard let jsonDictionary = jsonObject as? [String: Any] else {
                    print("Error converting to dictionary")
                    return nil
                }
                
                // print("json dictionary:")
                // print(jsonDictionary)
                
                return jsonDictionary
            } catch {
                print("[!] error loading json data: \(error.localizedDescription)")
                return nil
            }
        } else {
            print("[!] file not found")
            return nil
        }
    }
    
    func loadRecipes(debug: Bool=false) -> [Recipe] {
        var recipeDataArray = [Recipe]()
    
        let jsonDictionary = loadJSONData(from: "recipes")
        for (recipeName, url) in jsonDictionary ?? [:] {
            guard let link = url as? String
            else {
                continue
            }
            let recipeData = Recipe(name: recipeName, url: link)
            recipeDataArray.append(recipeData)
        }
        
        if debug == true {
            for recipe in recipeDataArray{
                print("Recipe Name: \(recipe.name)")
                print("Recipe Link: \(recipe.url)")
            }
        }
        return recipeDataArray
    }
    
    struct PreviewBox: View {
        var color: Color
        var recipe: Recipe
        
        var body: some View {
            Button(action: {
                print("selected preview:  \(recipe.url)")
            }) {
                HStack {
                    Image(systemName: "photo.on.rectangle")
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: 60, height: 120)
                        .padding()
                        .foregroundColor(.white)
                    Text(recipe.name)
                        .foregroundColor(.white)
                    Spacer()
                }
                .background(color)
                .cornerRadius(10)
            }
        }
    }
}

#Preview {
    RecipesView()
}
