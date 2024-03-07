//
//  SearchView.swift
//  project
//
//  Created by Drew S on 3/6/24.
//

import SwiftUI

struct SearchView: View {
    let boxGrey = Color(hex: 0x404040)
    let textGrey = Color(hex: 0x999999)
    
    @State private var searchText: String = ""
    
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
    }
}

#Preview {
    SearchView()
}
