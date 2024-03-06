//
//  HomeView.swift
//  project
//
//  Created by Drew S on 3/5/24.
//

import SwiftUI

extension Color {
    init(hex: UInt32) {
        let red = Double((hex & 0xFF0000) >> 16) / 255.0
        let green = Double((hex & 0x00FF00) >> 8) / 255.0
        let blue = Double(hex & 0x0000FF) / 255.0
        self.init(red: red, green: green, blue: blue)
    }
}

struct HomeView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)

    var body: some View {
        VStack{
            HStack() {
                Text("Hello Rupert!")
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
                
                HScroll()
                
                HStack{
                    Text("Popular foods")
                        .font(.title)
                        .foregroundColor(textGrey)
                    Spacer()
                }
                
                HScroll()

            }.padding(.horizontal, 10)
            

            Spacer()

            
        }.background(Color.black)
    }
}
struct HScroll: View {
    var body: some View{
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                let colorList: [Color] = [.red, .blue, .green, .yellow, .orange]

                ForEach(0..<10) { foodItem in
                    let index = Int.random(in: 0..<colorList.count)
                    let randomColor = colorList[index]
                    
                    ScrollBox(color: randomColor, description: "item \(foodItem)")
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
