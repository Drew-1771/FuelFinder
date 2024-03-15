//
//  SearchView.swift
//  project
//
//  Created by Drew S on 3/6/24.
//

import SwiftUI
import Foundation

struct Dish: Codable {
    let name: String
    let calories: Double
    let fat: Double
    let protein: Double
    let sugar: Double
    let carbs: Double
}
struct SearchView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)
    
    @State private var searchText: String = ""
    @State private var dishes: [Dish] = []
    
    var body: some View {
        VStack{
            VStack
            {
                HStack{
                    Spacer()
                    Image(systemName: "magnifyingglass").foregroundColor(textGrey)
                        .padding(.horizontal, 2)
                    TextField("Search", text: $searchText)
                        .padding()
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding(.horizontal, 2)
                    
                }
            }.background(Color.black)
            Spacer()
        }.background(Color.black)
            .onAppear{_ = loadDishes(debug: true)}
        .onChange(of: searchText) {
            search(searchText)
                }
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
                
                //print("json dictionary:")
                //print(jsonDictionary)
                
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
    
    func loadDishes(debug: Bool=false) -> [Dish]? {
        var dishDataArray = [Dish]()
        
        let jsonDictionary = loadJSONData(from: "dishes")
        for (dishName, nutritionInformation) in jsonDictionary ?? [:] {
            guard let nutritionDict = nutritionInformation as? [String: Any],
                  let calories = nutritionDict["calories"] as? Double,
                  let fat = nutritionDict["fat"] as? Double,
                  let protein = nutritionDict["protein"] as? Double,
                  let sugar = nutritionDict["sugar"] as? Double,
                  let carbs = nutritionDict["carbs"] as? Double else {
                continue
            }
            let dishData = Dish(name: dishName, calories: calories, fat: fat, protein: protein, sugar: sugar, carbs: carbs)
            dishDataArray.append(dishData)
        }
        
        if debug == true {
            for dish in dishDataArray{
                print("Dish Name: \(dish.name)")
                print("Calories: \(dish.calories)")
                print("Fat: \(dish.fat)")
                print("Protein: \(dish.protein)")
                print("Sugar: \(dish.sugar)")
                print("Carbs: \(dish.carbs)\n")
            }
        }
        return dishDataArray
    }
    
    func search(_ query: String)
    {
        // for string in query
        // calculate distances
        // return highest distance
        print(query)
    }
    
    func levenshteinDistanceScore(string1: String, string2: String) ->
        // based on solution graciously provided by Ankit Rathi at https://stackoverflow.com/questions/47794688/closest-match-string-array-sorting-in-swift
        Double {
            var s1 = string1.lowercased()
            var s2 = string2.lowercased()

            s1 = s1.trimmingCharacters(in: .whitespacesAndNewlines)
            s2 = s2.trimmingCharacters(in: .whitespacesAndNewlines)
            
            let empty = [Int](repeating:0, count: s2.count)
            var last = [Int](0...s2.count)

            for (i, t_lett) in s1.enumerated() {
                var current = [i + 1] + empty
                for (j, s_lett) in s2.enumerated() {
                    current[j + 1] = t_lett == s_lett ? last[j] : Swift.min(last[j], last[j + 1], current[j])+1
                }
                last = current
            }

            let lowestScore = max(s1.count, s2.count)

            if let validDistance = last.last {
                return  1 - (Double(validDistance) / Double(lowestScore))
            }

            return 0.0
        }
}

#Preview {
    SearchView()
}
