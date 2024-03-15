//
//  HomeView.swift
//  project
//
//  Created by Drew S on 3/5/24.
//

import SwiftUI


struct HomeView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)

    var body: some View {
        VStack{
            HStack() {
                Text("Hello User!")
                    .font(.title)
                    .foregroundColor(textGrey)
                    .padding()
                Spacer()
                SettingsCog(fgColor: .gray)
            }
            
            HStack {
                VStack(spacing: 20){
                    PreviewBox(color: boxGrey, description: "one")
                    PreviewBox(color: boxGrey, description:  "two")
                    PreviewBox(color: boxGrey, description: "three")
                }.padding(.horizontal, 2)
                
                VStack(spacing: 20){
                    PreviewBox(color: boxGrey, description:  "four")
                    PreviewBox(color: boxGrey, description:  "five")
                    PreviewBox(color: boxGrey, description:  "six")
                }.padding(.horizontal, 2)
            }
            .padding(.horizontal, 20)
            
            VStack {
                HStack{
                    Text("Recommended for you")
                        .font(.title)
                        .foregroundColor(textGrey)
                    Spacer()
                }
                HScroll(forward: true, recommendations: loadRecommendationsForYou())
                
                HStack{
                    Text("Popular foods")
                        .font(.title)
                        .foregroundColor(textGrey)
                    Spacer()
                }
                
               HScroll(forward: false, recommendations: loadRecommendationsPopular())

            }.padding(.horizontal, 10)
            

            Spacer()

            
        }.background(Color.black)
    }
    
    func loadJSONData(from filename: String) -> [String: String]? {
        if let url = Bundle.main.url(forResource: filename, withExtension: "json") {
            do {
                let data = try Data(contentsOf: url)
                // convert json data to any object
                let jsonObject = try JSONSerialization.jsonObject(with: data, options: [])
                //print("json object:")
                //print(jsonObject)
                
                // convert any object to [String: Any] dictionary
                guard let jsonDictionary = jsonObject as? [String: String] else {
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
    
    func loadRecommendationsForYou(debug: Bool=false) -> [String] {
        var recommendationDataArray = [String]()

        if let jsonDictionary = loadJSONData(from: "recommendation_user") {
            let sortedKeys = Array(jsonDictionary.keys).sorted(by: { $0 < $1 })
            for key in sortedKeys {
                if let dishName = jsonDictionary[key] {
                    recommendationDataArray.append(dishName)
                }
            }
        }
        
        if debug == true {
            for dish in recommendationDataArray{
                print(dish)
            }
        }
        return recommendationDataArray
    }
    
    func loadRecommendationsPopular(debug: Bool=false) -> [String] {
        var recommendationDataArray = [String]()

        if let jsonDictionary = loadJSONData(from: "recommendation_popular") {
            let sortedKeys = Array(jsonDictionary.keys).sorted(by: { $0 < $1 })
            for key in sortedKeys {
                if let dishName = jsonDictionary[key] {
                    recommendationDataArray.append(dishName)
                }
            }
        }
        
        if debug == true {
            for dish in recommendationDataArray{
                print(dish)
            }
        }
        return recommendationDataArray
    }
    
}

struct HScroll: View {
    let forward: Bool
    let recommendations: [String]
    
    var body: some View{
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                let colorList: [Color] = [.red, .blue, .green, .yellow, .orange]
                let colorListB: [Color] = [.orange, .mint, .red, .green, .yellow]
                
                if forward == true {
                    ForEach(Array(colorList.enumerated()), id: \.offset) { index, color in
                        ScrollBox(color: color, description: " \(recommendations[index])")
                    }
                }
                else
                {
                    ForEach(Array(colorListB.enumerated()), id: \.offset) { index, color in ScrollBox(color: color, description: " \(recommendations[index])")
                    }
                }
            }
            .padding(.horizontal, 10)
        }
    }
}

struct PreviewBox: View {
    var color: Color
    var description: String
    
    var body: some View {
        Button(action: {
            print("selected preview: \(description)")
        }) {
            HStack {
                Image(systemName: "photo.on.rectangle")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 30, height: 30)
                    .padding()
                    .foregroundColor(.white)
                Text(description)
                    .foregroundColor(.white)
                    .padding()
                Spacer()
            }
            .background(color)
            .cornerRadius(10)
        }
    }
}

struct ScrollBox: View {
    var color: Color
    var description: String
    
    var body: some View {
        Button(action: {
            print("selected preview: \(description)")
        }) {
            HStack {
                Image(systemName: "photo.on.rectangle")
                    .resizable()
                    .aspectRatio(contentMode: .fit)
                    .frame(width: 100, height: 100)
                    .padding()
                    .foregroundColor(.white)
                Spacer()
            }
            .background(color)
            .cornerRadius(10)
        }
    }
}

struct SettingsCog: View {
    var fgColor: Color

    var body: some View {
        Button(action: {
            print("selected settings")
        }) {
            Image(systemName: "gearshape")
                .resizable()
                .aspectRatio(contentMode: .fit)
                .frame(width: 30, height: 30)
                .foregroundColor(fgColor)
                .padding(.horizontal, 25)
        }
    }
    
}

#Preview {
    HomeView()
}
